import React, { useMemo, useState } from "react";

const tData = {
  ru: {
    language: "Язык",
    russian: "Русский",
    english: "English",
    createAccount: "Создать аккаунт",
    loginTitle: "IzvestNick",
    phone: "Номер телефона",
    password: "Пароль",
    confirmPassword: "Подтвердите пароль",
    ok: "ОК",
    name: "Имя",
    surname: "Фамилия",
    continue: "Продолжить",
    chats: "Чаты",
    contacts: "Контакты",
    profile: "Профиль",
    search: "Поиск",
    writeMessage: "Напишите сообщение...",
    createLink: "Создать свой линк",
    uploadPhoto: "Загрузить фото",
    changeMainPhoto: "Сменить главное фото",
    addPhoto: "Добавить фото",
    photosLimit: "До 30 фото в профиле",
    deleteForMe: "Удалить только у себя",
    deleteForBoth: "Удалить у обоих",
    forward: "Переслать",
    reply: "Ответить",
    signIn: "Войти",
    countryCode: "Код страны",
    noMatch: "Пароли не совпадают",
    send: "Отправить",
  },
  en: {
    language: "Language",
    russian: "Русский",
    english: "English",
    createAccount: "Create account",
    loginTitle: "IzvestNick",
    phone: "Phone number",
    password: "Password",
    confirmPassword: "Confirm password",
    ok: "OK",
    name: "First name",
    surname: "Last name",
    continue: "Continue",
    chats: "Chats",
    contacts: "Contacts",
    profile: "Profile",
    search: "Search",
    writeMessage: "Write a message...",
    createLink: "Create your link",
    uploadPhoto: "Upload photo",
    changeMainPhoto: "Change main photo",
    addPhoto: "Add photo",
    photosLimit: "Up to 30 profile photos",
    deleteForMe: "Delete for me",
    deleteForBoth: "Delete for both",
    forward: "Forward",
    reply: "Reply",
    signIn: "Sign in",
    countryCode: "Country code",
    noMatch: "Passwords do not match",
    send: "Send",
  },
};

const countryCodes = [
  { code: "+1", flag: "🇺🇸" },
  { code: "+7", flag: "🇷🇺" },
  { code: "+44", flag: "🇬🇧" },
  { code: "+49", flag: "🇩🇪" },
  { code: "+33", flag: "🇫🇷" },
  { code: "+34", flag: "🇪🇸" },
  { code: "+39", flag: "🇮🇹" },
  { code: "+31", flag: "🇳🇱" },
  { code: "+81", flag: "🇯🇵" },
  { code: "+86", flag: "🇨🇳" },
  { code: "+91", flag: "🇮🇳" },
  { code: "+971", flag: "🇦🇪" },
];

const seedChats = [
  { id: 1, name: "Nora Vale", last: "Жду макет нового экрана профиля.", messages: [{ id: 1, author: "them", text: "Привет!" }] },
  { id: 2, name: "Product Team", last: "Созвон в 18:00 подтверждён.", messages: [{ id: 2, author: "them", text: "Созвон в 18:00 подтверждён." }] },
];

export default function MessengerWebMVP() {
  const [lang, setLang] = useState("ru");
  const [screen, setScreen] = useState("login");
  const [countryCode, setCountryCode] = useState("+7");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [selectedChatId, setSelectedChatId] = useState(1);
  const [message, setMessage] = useState("");
  const [profileLink, setProfileLink] = useState("@izvestnick");
  const [chats, setChats] = useState(seedChats);
  const t = tData[lang];

  const selectedChat = useMemo(() => chats.find((c) => c.id === selectedChatId) || chats[0], [chats, selectedChatId]);

  const onCreateAccount = () => {
    if (password !== confirmPassword) {
      alert(t.noMatch);
      return;
    }
    setScreen("profile-setup");
  };

  const onFinishProfile = () => setScreen("messenger");

  const onSend = () => {
    if (!message.trim()) return;
    setChats((prev) => prev.map((c) => c.id === selectedChatId ? { ...c, last: message, messages: [...c.messages, { id: Date.now(), author: "me", text: message }] } : c));
    setMessage("");
  };

  if (screen === "login") {
    return <div style={styles.wrap}><TopBar t={t} setLang={setLang} setScreen={setScreen} /><Card><h1>{t.loginTitle}</h1><div>{t.countryCode}</div><CountryCodes value={countryCode} onChange={setCountryCode} /><input style={styles.input} value={phone} onChange={(e) => setPhone(e.target.value)} placeholder={`${countryCode} 999 123 45 67`} /><input style={styles.input} type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder={t.password} /><button style={styles.button} onClick={() => setScreen("messenger")}>{t.ok}</button></Card></div>;
  }

  if (screen === "signup") {
    return <div style={styles.wrap}><TopBar t={t} setLang={setLang} setScreen={setScreen} /><Card><h1>{t.createAccount}</h1><div>{t.countryCode}</div><CountryCodes value={countryCode} onChange={setCountryCode} /><input style={styles.input} value={phone} onChange={(e) => setPhone(e.target.value)} placeholder={`${countryCode} 999 123 45 67`} /><input style={styles.input} type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder={t.password} /><input style={styles.input} type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} placeholder={t.confirmPassword} /><button style={styles.button} onClick={onCreateAccount}>{t.ok}</button></Card></div>;
  }

  if (screen === "profile-setup") {
    return <div style={styles.wrap}><TopBar t={t} setLang={setLang} setScreen={setScreen} /><Card><h1>{t.profile}</h1><input style={styles.input} value={name} onChange={(e) => setName(e.target.value)} placeholder={t.name} /><input style={styles.input} value={surname} onChange={(e) => setSurname(e.target.value)} placeholder={t.surname} /><button style={styles.button} onClick={onFinishProfile}>{t.continue}</button></Card></div>;
  }

  return (
    <div style={{ ...styles.wrap, alignItems: "stretch" }}>
      <div style={styles.sidebar}>
        <h3>{t.chats}</h3>
        {chats.map((chat) => <div key={chat.id} style={styles.chatItem} onClick={() => setSelectedChatId(chat.id)}><b>{chat.name}</b><div>{chat.last}</div></div>)}
      </div>
      <div style={styles.main}>
        <h3>{selectedChat.name}</h3>
        <div style={styles.msgList}>{selectedChat.messages.map((m) => <div key={m.id} style={m.author === "me" ? styles.myMsg : styles.theirMsg}>{m.text}</div>)}</div>
        <textarea style={styles.textarea} value={message} onChange={(e) => setMessage(e.target.value)} placeholder={t.writeMessage} />
        <button style={styles.button} onClick={onSend}>{t.send}</button>
      </div>
      <div style={styles.right}>
        <h3>{t.profile}</h3>
        <div>{profileLink}</div>
        <button style={styles.ghost}>{t.createLink}</button>
        <button style={styles.ghost}>{t.uploadPhoto}</button>
        <button style={styles.ghost}>{t.changeMainPhoto}</button>
        <button style={styles.ghost}>{t.addPhoto}</button>
        <div>{t.photosLimit}</div>
      </div>
    </div>
  );
}

function TopBar({ t, setLang, setScreen }) {
  return <div style={styles.top}><div><button style={styles.ghost} onClick={() => setLang("ru")}>{t.russian}</button><button style={styles.ghost} onClick={() => setLang("en")}>{t.english}</button></div><button style={styles.button} onClick={() => setScreen("signup")}>{t.createAccount}</button></div>;
}

function CountryCodes({ value, onChange }) {
  return <div style={styles.codes}>{countryCodes.map((c) => <button key={c.code} style={{ ...styles.codeBtn, background: value === c.code ? "#111827" : "#fff", color: value === c.code ? "#fff" : "#111827" }} onClick={() => onChange(c.code)}>{c.flag} {c.code}</button>)}</div>;
}

function Card({ children }) { return <div style={styles.card}>{children}</div>; }

const styles = {
  wrap: { minHeight: "100vh", display: "flex", gap: 16, padding: 24, background: "#eef2ff", fontFamily: "Arial, sans-serif" },
  top: { position: "fixed", top: 16, left: 16, right: 16, display: "flex", justifyContent: "space-between" },
  card: { width: 520, margin: "80px auto", background: "white", padding: 24, borderRadius: 24, boxShadow: "0 10px 30px rgba(0,0,0,.08)", display: "grid", gap: 12 },
  input: { height: 44, borderRadius: 14, border: "1px solid #cbd5e1", padding: "0 14px" },
  textarea: { minHeight: 120, borderRadius: 14, border: "1px solid #cbd5e1", padding: 14, width: "100%" },
  button: { height: 42, borderRadius: 14, border: 0, padding: "0 16px", background: "#111827", color: "white", cursor: "pointer" },
  ghost: { height: 38, borderRadius: 12, border: "1px solid #cbd5e1", padding: "0 12px", background: "white", cursor: "pointer", marginRight: 8, marginTop: 8 },
  codes: { display: "flex", flexWrap: "wrap", gap: 8 },
  codeBtn: { height: 38, borderRadius: 12, border: "1px solid #cbd5e1", padding: "0 12px", cursor: "pointer" },
  sidebar: { width: 320, background: "#111827", color: "white", borderRadius: 24, padding: 16 },
  main: { flex: 1, background: "white", borderRadius: 24, padding: 16, display: "flex", flexDirection: "column", gap: 12 },
  right: { width: 300, background: "white", borderRadius: 24, padding: 16 },
  chatItem: { padding: 12, borderRadius: 16, background: "rgba(255,255,255,.08)", marginBottom: 8, cursor: "pointer" },
  msgList: { flex: 1, minHeight: 300, background: "#f8fafc", borderRadius: 16, padding: 12 },
  myMsg: { marginLeft: "auto", maxWidth: "70%", padding: 12, borderRadius: 16, background: "#111827", color: "white", marginBottom: 8 },
  theirMsg: { maxWidth: "70%", padding: 12, borderRadius: 16, background: "#e2e8f0", color: "#111827", marginBottom: 8 },
};
