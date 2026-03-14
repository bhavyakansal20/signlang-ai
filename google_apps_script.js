// ============================================================
// SignLang AI — Google Apps Script Backend
// Paste this ENTIRE script in:
//   Extensions → Apps Script → replace everything → Save → Deploy
// ============================================================

const SHEET_ID = "1LGyBz3AduBFOB0JMqSJ6GRL902TUIO7zNrPOlzAm33w";

function getSheet(name) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    if (name === "Users")
      sheet.appendRow(["name", "email", "password_hash", "created_at"]);
    else if (name === "Sessions")
      sheet.appendRow(["email", "name", "date", "time", "words", "word_count", "sentence", "duration"]);
    else if (name === "Feedback")
      sheet.appendRow(["email", "name", "rating", "message", "timestamp"]);
    sheet.setFrozenRows(1);
    const h = sheet.getRange(1, 1, 1, 8);
    h.setBackground("#0D1117");
    h.setFontColor("#FFFFFF");
    h.setFontWeight("bold");
  }
  return sheet;
}

function sheetToObjects(sheet) {
  const data = sheet.getDataRange().getValues();
  if (data.length <= 1) return [];
  const headers = data[0];
  return data.slice(1).map(row => {
    const obj = {};
    headers.forEach((h, i) => { obj[h] = row[i]; });
    return obj;
  });
}

function jsonResponse(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    const params = JSON.parse(e.postData.contents);
    const action = params.action;
    if (action === "signup")       return jsonResponse(handleSignup(params));
    if (action === "signin")       return jsonResponse(handleSignin(params));
    if (action === "add_session")  return jsonResponse(handleAddSession(params));
    if (action === "get_sessions") return jsonResponse(handleGetSessions(params));
    if (action === "add_feedback") return jsonResponse(handleAddFeedback(params));
    return jsonResponse({ status: "error", message: "Unknown action: " + action });
  } catch (err) {
    return jsonResponse({ status: "error", message: err.toString() });
  }
}

function doGet(e) {
  return jsonResponse({ status: "ok", message: "SignLang AI Sheets API is running." });
}

function handleSignup(params) {
  const sheet   = getSheet("Users");
  const records = sheetToObjects(sheet);
  const exists  = records.find(r =>
    String(r.email).trim().toLowerCase() === String(params.email).trim().toLowerCase());
  if (exists) return { status: "error", message: "Email already registered." };
  sheet.appendRow([params.name||"", params.email||"", params.password_hash||"", params.created_at||new Date().toISOString()]);
  return { status: "ok", message: "Account created." };
}

function handleSignin(params) {
  const sheet   = getSheet("Users");
  const records = sheetToObjects(sheet);
  const user    = records.find(r =>
    String(r.email).trim().toLowerCase() === String(params.email).trim().toLowerCase());
  if (!user) return { status: "error", message: "No account found with this email." };
  if (String(user.password_hash).trim() !== String(params.password_hash).trim())
    return { status: "error", message: "Incorrect password." };
  return { status: "ok", user: { name: user.name, email: user.email } };
}

function handleAddSession(params) {
  const sheet = getSheet("Sessions");
  sheet.appendRow([params.email||"", params.name||"", params.date||"", params.time||"",
    params.words||"", params.word_count||"0", params.sentence||"", params.duration||"0"]);
  return { status: "ok", message: "Session saved." };
}

function handleGetSessions(params) {
  const sheet   = getSheet("Sessions");
  const records = sheetToObjects(sheet);
  const email   = String(params.email).trim().toLowerCase();
  const list    = records.filter(r =>
    String(r.email).trim().toLowerCase() === email).reverse();
  return { status: "ok", sessions: list };
}

function handleAddFeedback(params) {
  const sheet = getSheet("Feedback");
  sheet.appendRow([params.email||"", params.name||"", params.rating||"",
    params.message||"", params.timestamp||new Date().toISOString()]);
  return { status: "ok", message: "Feedback saved." };
}
