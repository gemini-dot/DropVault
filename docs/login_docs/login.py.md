# Fetching Data từ trang Login — DevDrop

Tài liệu này giải thích cách trang `login.html` lưu trữ và truy xuất dữ liệu tài khoản, và cách tích hợp với backend thực tế.

---

## 1. Dữ liệu được lưu ở đâu?

Trang login hiện tại dùng **`localStorage`** của trình duyệt để lưu danh sách tài khoản đã đăng nhập.

```js
const STORAGE_KEY = 'dd_saved_accounts';

// Đọc
const accounts = JSON.parse(localStorage.getItem('dd_saved_accounts') || '[]');

// Ghi
localStorage.setItem('dd_saved_accounts', JSON.stringify(accounts));
```

Mỗi account object có cấu trúc:

```js
{
  id:        "acc1",                    // unique ID
  name:      "Nguyễn Văn Minh",
  email:     "minhnv@gmail.com",
  provider:  "google" | "github" | "email",
  avatar:    "https://..." | null,
  lastLogin: 1712345678000              // Unix timestamp (ms)
}
```

---

## 2. Tích hợp API thực tế

### 2.1 Đăng nhập bằng Email / Password

Thay hàm `submitLogin()` trong `login.html`:

```js
async function submitLogin() {
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-pw').value;

  if (!email || !password) return;
  setLoading('login-btn', true);

  try {
    const res = await fetch('https://api.devdrop.sh/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include'   // gửi kèm cookie nếu dùng session
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.message || 'Login failed');
    }

    const data = await res.json();
    // data = { token: "eyJ...", user: { id, name, email, avatar } }

    // Lưu token
    localStorage.setItem('dd_token', data.token);

    // Lưu account vào danh sách saved
    addAccount({
      id: data.user.id,
      name: data.user.name,
      email: data.user.email,
      provider: 'email',
      avatar: data.user.avatar || null,
    });

    // Chuyển sang 2FA hoặc dashboard
    showPane('pane-2fa');

  } catch (err) {
    toast('Đăng nhập thất bại', err.message, '!');
  } finally {
    setLoading('login-btn', false);
  }
}
```

---

### 2.2 Đăng nhập bằng Google / GitHub (OAuth 2.0)

Flow chuẩn: **Redirect → Callback → Token**.

```js
function oauthLogin(provider) {
  // Redirect trình duyệt đến OAuth endpoint
  const callbackUrl = encodeURIComponent('https://devdrop.sh/auth/callback');
  window.location.href =
    `https://api.devdrop.sh/auth/${provider}?redirect_uri=${callbackUrl}`;
}
```

**Trang callback** (`/auth/callback`) nhận `?code=...` từ Google/GitHub, server đổi lấy token, rồi redirect về:

```
https://devdrop.sh/login?token=eyJ...&name=Jane&email=jane@gmail.com&avatar=https://...
```

**Đọc token từ URL** (thêm vào cuối `init` trong `login.html`):

```js
(function readOauthCallback() {
  const p = new URLSearchParams(location.search);
  const token = p.get('token');
  if (!token) return;

  localStorage.setItem('dd_token', token);

  addAccount({
    id: 'acc' + Date.now(),
    name:     p.get('name')   || 'User',
    email:    p.get('email')  || '',
    provider: p.get('provider') || 'google',
    avatar:   p.get('avatar') || null,
  });

  // Xóa params khỏi URL rồi chuyển trang
  history.replaceState({}, '', '/login');
  window.location.href = '/dashboard';
})();
```

---

### 2.3 Xác thực OTP / 2FA

```js
async function submitOtp() {
  const otp = [...document.querySelectorAll('.otp-input')]
    .map(i => i.value).join('');

  if (otp.length < 6) return;
  setLoading('otp-btn', true);

  try {
    const res = await fetch('https://api.devdrop.sh/auth/verify-otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('dd_token')}`
      },
      body: JSON.stringify({ otp })
    });

    if (!res.ok) throw new Error('Invalid code');

    const data = await res.json();
    localStorage.setItem('dd_token', data.token); // token mới sau 2FA
    window.location.href = '/dashboard';

  } catch (err) {
    toast('Mã không hợp lệ', 'Vui lòng thử lại.', '!');
    document.querySelectorAll('.otp-input').forEach(i => i.value = '');
    document.querySelector('.otp-input').focus();
  } finally {
    setLoading('otp-btn', false);
  }
}
```

---

### 2.4 Đăng ký tài khoản mới

```js
async function submitRegister() {
  const body = {
    firstName: document.getElementById('reg-first').value.trim(),
    lastName:  document.getElementById('reg-last').value.trim(),
    email:     document.getElementById('reg-email').value.trim(),
    password:  document.getElementById('reg-pw').value,
  };

  setLoading('reg-btn', true);

  try {
    const res = await fetch('https://api.devdrop.sh/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.message || 'Registration failed');
    }

    const data = await res.json();
    localStorage.setItem('dd_token', data.token);

    addAccount({
      id: data.user.id,
      name: `${body.firstName} ${body.lastName}`.trim(),
      email: body.email,
      provider: 'email',
      avatar: null,
    });

    showPane('pane-2fa');
    toast('Tài khoản đã tạo', 'Kiểm tra email để xác thực.', '◈');

  } catch (err) {
    toast('Đăng ký thất bại', err.message, '!');
  } finally {
    setLoading('reg-btn', false);
  }
}
```

---

### 2.5 Quên mật khẩu

```js
async function submitForgot() {
  const email = document.getElementById('forgot-email').value.trim();

  try {
    await fetch('https://api.devdrop.sh/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    toast('Email đã gửi', `Kiểm tra ${email} để reset mật khẩu.`, '◈');
    showPane('pane-accounts');
  } catch {
    toast('Lỗi', 'Không thể gửi email. Thử lại sau.', '!');
  }
}
```

---

## 3. Lấy danh sách Saved Accounts từ server

Nếu muốn đồng bộ danh sách tài khoản đã đăng nhập **qua nhiều thiết bị**, gọi API khi trang load:

```js
async function loadRemoteAccounts() {
  const token = localStorage.getItem('dd_token');
  if (!token) return; // chưa đăng nhập lần nào

  try {
    const res = await fetch('https://api.devdrop.sh/auth/sessions', {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!res.ok) return;

    const data = await res.json();
    // data.sessions = [{ id, name, email, provider, lastLogin, avatar }, ...]

    // Merge với localStorage — ưu tiên server
    const local  = getAccounts();
    const remote = data.sessions;

    // Dùng email làm key dedup
    const merged = [
      ...remote,
      ...local.filter(l => !remote.find(r => r.email === l.email))
    ];

    saveAccounts(merged);
    renderAccounts();

  } catch (err) {
    console.warn('Could not sync sessions:', err);
    // Fallback về localStorage — không crash UI
  }
}

// Gọi khi trang load
loadRemoteAccounts();
```

---

## 4. Bảo vệ Token

| Cách lưu          | An toàn? | Ghi chú |
|-------------------|----------|---------|
| `localStorage`    | ⚠️ Trung bình | Dễ bị XSS đọc, nhưng phổ biến |
| `sessionStorage`  | ⚠️ Tương tự | Mất khi đóng tab |
| `httpOnly cookie` | ✅ Tốt nhất | Server set, JS không đọc được |
| Memory (biến JS)  | ✅ Tốt | Mất khi reload, cần refresh token |

**Khuyến nghị**: Dùng `httpOnly` cookie cho `access_token` (server set qua `Set-Cookie`), dùng `localStorage` chỉ để lưu metadata hiển thị (tên, avatar) — không lưu token nhạy cảm.

---

## 5. Xử lý lỗi chuẩn

```js
async function apiFetch(url, options = {}) {
  const token = localStorage.getItem('dd_token');

  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    }
  });

  if (res.status === 401) {
    // Token hết hạn → xóa và redirect về login
    localStorage.removeItem('dd_token');
    window.location.href = '/login?expired=1';
    return;
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(err.message);
  }

  return res.json();
}

// Dùng:
const data = await apiFetch('https://api.devdrop.sh/user/me');
```

---

## 6. Tóm tắt các endpoints cần có

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/auth/login` | Đăng nhập email/password |
| `POST` | `/auth/register` | Tạo tài khoản mới |
| `POST` | `/auth/logout` | Đăng xuất, xóa session |
| `POST` | `/auth/verify-otp` | Xác thực mã 2FA |
| `POST` | `/auth/resend-otp` | Gửi lại mã OTP |
| `POST` | `/auth/forgot-password` | Gửi link reset mật khẩu |
| `POST` | `/auth/reset-password` | Đặt lại mật khẩu mới |
| `GET`  | `/auth/google` | Bắt đầu OAuth Google |
| `GET`  | `/auth/github` | Bắt đầu OAuth GitHub |
| `GET`  | `/auth/callback` | Nhận code từ OAuth provider |
| `GET`  | `/auth/sessions` | Lấy danh sách phiên đăng nhập |
| `GET`  | `/user/me` | Thông tin user hiện tại |