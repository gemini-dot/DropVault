/* ════════════════════════════════════
   SAVED ACCOUNTS DATA (localStorage)
════════════════════════════════════ */
const STORAGE_KEY='dd_saved_accounts';

// Default demo accounts so UI is never empty on first load
const DEFAULT_ACCOUNTS=[
  {id:'acc1',name:'Nguyễn Văn Minh',email:'minhnv@gmail.com',provider:'google',avatar:null,lastLogin:Date.now()-3600000},
  {id:'acc2',name:'Alex K.',email:'alex@company.io',provider:'github',avatar:null,lastLogin:Date.now()-86400000*2},
  {id:'acc3',name:'Sophie Chen',email:'sophie.chen@devmail.sh',provider:'email',avatar:null,lastLogin:Date.now()-86400000*7},
];

function getAccounts(){
  try{
    const raw=localStorage.getItem(STORAGE_KEY);
    if(raw){const a=JSON.parse(raw);if(a.length)return a;}
  }catch(e){}
  return DEFAULT_ACCOUNTS;
}
function saveAccounts(list){
  localStorage.setItem(STORAGE_KEY,JSON.stringify(list));
}
function addAccount(acc){
  const list=getAccounts().filter(a=>a.email!==acc.email);
  list.unshift({...acc,lastLogin:Date.now()});
  saveAccounts(list.slice(0,8));// max 8 saved
}
function removeAccount(id){
  saveAccounts(getAccounts().filter(a=>a.id!==id));
  renderAccounts();
  toast('Account removed','Removed from saved accounts.','○');
}

/* ── Initials from name ── */
function initials(name){
  if(!name)return'?';
  return name.split(' ').slice(0,2).map(n=>n[0]).join('').toUpperCase();
}

/* ── Provider label ── */
function providerLabel(p){
  if(p==='google')return'G ·';
  if(p==='github')return'⬡ ·';
  return'@ ·';
}

/* ════════════════════════════════════
   RENDER ACCOUNTS
════════════════════════════════════ */
function renderAccounts(){
  const list=getAccounts();
  const el=document.getElementById('accounts-list');
  if(!list.length){
    document.getElementById('saved-section').style.display='none';
    return;
  }
  document.getElementById('saved-section').style.display='';
  el.innerHTML=list.map(a=>`
    <div class="account-row" id="row-${a.id}" onclick="selectAccount('${a.id}')" tabindex="0" role="button" aria-label="Sign in as ${a.email}">
      <div class="acc-avatar">
        ${a.avatar
          ?`<img src="${a.avatar}" alt="${a.name}" onerror="this.style.display='none'">`
          :''}
        <div class="acc-avatar-fallback">${initials(a.name)}</div>
      </div>
      <div class="acc-info">
        <div class="acc-name">${escHtml(a.name)}</div>
        <div class="acc-email">${escHtml(a.email)}</div>
      </div>
      <div class="acc-provider">${providerLabel(a.provider)} ${capitalize(a.provider)}</div>
      <div class="acc-end">
        <div class="acc-check">✓</div>
        <button class="acc-remove" onclick="event.stopPropagation();removeAccount('${a.id}')" title="Remove account" type="button">✕</button>
      </div>
    </div>`).join('')+`
    <button class="add-account-btn" onclick="showPane('pane-login')" type="button">
      <div class="add-icon">+</div>
      <span>Use a different account</span>
    </button>`;
}

/* ════════════════════════════════════
   EMAIL SUGGESTIONS
════════════════════════════════════ */
function renderEmailDropdown(query){
  const list=getAccounts();
  const dd=document.getElementById('email-dropdown');
  const filtered=query
    ?list.filter(a=>a.email.toLowerCase().includes(query.toLowerCase())||a.name.toLowerCase().includes(query.toLowerCase()))
    :list;
  if(!filtered.length){dd.innerHTML='';return;}
  dd.innerHTML=filtered.map(a=>`
    <div class="email-option" onmousedown="pickEmail('${escAttr(a.email)}')">
      <div class="email-option-avatar">${initials(a.name)}</div>
      <div class="email-option-info">
        <div class="email-option-email">${escHtml(a.email)}</div>
        <div class="email-option-name">${escHtml(a.name)}</div>
      </div>
    </div>`).join('');
}
function openEmailDropdown(){
  renderEmailDropdown(document.getElementById('login-email').value);
  document.getElementById('email-dropdown').classList.add('open');
}
function closeEmailDropdown(){
  document.getElementById('email-dropdown').classList.remove('open');
}
function filterEmailSuggestions(val){
  renderEmailDropdown(val);
  if(!document.getElementById('email-dropdown').classList.contains('open'))
    document.getElementById('email-dropdown').classList.add('open');
}
function pickEmail(email){
  document.getElementById('login-email').value=email;
  closeEmailDropdown();
  document.getElementById('login-pw').focus();
}

/* ════════════════════════════════════
   SELECT SAVED ACCOUNT
════════════════════════════════════ */
function selectAccount(id){
  document.querySelectorAll('.account-row').forEach(r=>r.classList.remove('selected'));
  const row=document.getElementById('row-'+id);
  if(row)row.classList.add('selected');
  const acc=getAccounts().find(a=>a.id===id);
  if(!acc)return;
  // Simulate: go to 2FA for email accounts, direct for OAuth
  if(acc.provider==='email'){
    document.getElementById('login-email').value=acc.email;
    showPane('pane-login');
    setTimeout(()=>document.getElementById('login-pw').focus(),100);
  }else{
    // OAuth re-auth simulation
    document.getElementById('verify-email-label').textContent=acc.email;
    simulateOauthReauth(acc);
  }
}
function simulateOauthReauth(acc){
  setLoading(null,true,'pane-accounts');// visual
  setTimeout(()=>{
    setLoading(null,false,'pane-accounts');
    addAccount(acc);
    toast('Signed in','Welcome back, '+acc.name.split(' ')[0]+'!','◈');
    setTimeout(()=>window.location.href='index.html',1200);
  },1600);
}

/* ════════════════════════════════════
   PANE NAVIGATION
════════════════════════════════════ */
function showPane(id){
  document.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  // Update footer
  const footer=document.getElementById('card-footer');
  if(id==='pane-accounts')footer.style.display='';
  else if(id==='pane-forgot')footer.style.display='none';
  else if(id==='pane-2fa')footer.style.display='none';
  else footer.style.display='';
}

/* ════════════════════════════════════
   TAB SWITCHING
════════════════════════════════════ */
function switchTab(tab){
  document.querySelectorAll('.tab-btn').forEach((b,i)=>{
    b.classList.toggle('active',(i===0&&tab==='login')||(i===1&&tab==='register'));
  });
  document.getElementById('tab-login').style.display=tab==='login'?'':'none';
  document.getElementById('tab-register').style.display=tab==='register'?'':'none';
}

/* ════════════════════════════════════
   OAUTH LOGIN
════════════════════════════════════ */
function oauthLogin(provider){
  const btn=event.currentTarget;
  btn.style.opacity='.6';btn.style.pointerEvents='none';
  toast('Redirecting…','Opening '+capitalize(provider)+' sign-in…',provider==='google'?'G':'⬡');
  setTimeout(()=>{
    // Simulate successful OAuth return
    const mockAcc={
      id:'acc'+Date.now(),
      name:provider==='google'?'Google User':'GitHub User',
      email:provider==='google'?'user@gmail.com':'user@github.com',
      provider,avatar:null
    };
    addAccount(mockAcc);
    btn.style.opacity='';btn.style.pointerEvents='';
    toast('Signed in','Welcome to DevDrop!','◈');
    setTimeout(()=>window.location.href='index.html',1000);
  },2200);
}

/* ════════════════════════════════════
   EMAIL LOGIN
════════════════════════════════════ */
function submitLogin(){
  const email=document.getElementById('login-email').value.trim();
  const pw=document.getElementById('login-pw').value;
  if(!email){shake('login-email');toast('Email required','Enter your email address.','!');return;}
  if(!isValidEmail(email)){shake('login-email');toast('Invalid email','Enter a valid email address.','!');return;}
  if(!pw){shake('login-pw');toast('Password required','Enter your password.','!');return;}
  setLoading('login-btn',true);
  setTimeout(()=>{
    setLoading('login-btn',false);
    const remember=document.getElementById('remember-check').classList.contains('checked');
    if(remember){
      addAccount({id:'acc'+Date.now(),name:email.split('@')[0],email,provider:'email',avatar:null});
    }
    // Show 2FA
    document.getElementById('verify-email-label').textContent=email;
    showPane('pane-2fa');
    setTimeout(()=>document.querySelector('.otp-input').focus(),100);
  },1400);
}

/* ════════════════════════════════════
   REGISTER
════════════════════════════════════ */
function submitRegister(){
  const first=document.getElementById('reg-first').value.trim();
  const last=document.getElementById('reg-last').value.trim();
  const email=document.getElementById('reg-email').value.trim();
  const pw=document.getElementById('reg-pw').value;
  const pw2=document.getElementById('reg-pw2').value;
  const agreed=document.getElementById('terms-check').classList.contains('checked');
  if(!first){shake('reg-first');return;}
  if(!email||!isValidEmail(email)){shake('reg-email');toast('Invalid email','Enter a valid email.','!');return;}
  if(pw.length<8){shake('reg-pw');toast('Password too short','Use at least 8 characters.','!');return;}
  if(pw!==pw2){shake('reg-pw2');toast('Passwords don\'t match','Both passwords must be identical.','!');return;}
  if(!agreed){toast('Terms required','Please accept our Terms of Service.','!');return;}
  setLoading('reg-btn',true);
  setTimeout(()=>{
    setLoading('reg-btn',false);
    addAccount({id:'acc'+Date.now(),name:(first+' '+last).trim(),email,provider:'email',avatar:null});
    document.getElementById('verify-email-label').textContent=email;
    showPane('pane-2fa');
    toast('Account created','Check your email for the verification code.','◈');
    setTimeout(()=>document.querySelector('.otp-input').focus(),100);
  },1600);
}

/* ════════════════════════════════════
   FORGOT PASSWORD
════════════════════════════════════ */
function submitForgot(){
  const email=document.getElementById('forgot-email').value.trim();
  if(!email||!isValidEmail(email)){shake('forgot-email');toast('Invalid email','Enter your email address.','!');return;}
  const btn=document.querySelector('#pane-forgot .btn-submit');
  btn.classList.add('loading');
  setTimeout(()=>{
    btn.classList.remove('loading');
    toast('Email sent','Check '+email+' for a reset link.','◈');
    setTimeout(()=>showPane('pane-accounts'),800);
  },1500);
}

/* ════════════════════════════════════
   OTP
════════════════════════════════════ */
function otpMove(input,idx){
  input.value=input.value.replace(/\D/g,'');
  if(input.value&&idx<6){
    const inputs=document.querySelectorAll('.otp-input');
    inputs[idx].focus();
  }
  // Auto-submit when all filled
  const vals=[...document.querySelectorAll('.otp-input')].map(i=>i.value);
  if(vals.every(v=>v.length===1))submitOtp();
}
function otpBack(input,e){
  if(e.key==='Backspace'&&!input.value){
    const inputs=[...document.querySelectorAll('.otp-input')];
    const idx=inputs.indexOf(input);
    if(idx>0)inputs[idx-1].focus();
  }
}
function submitOtp(){
  const otp=[...document.querySelectorAll('.otp-input')].map(i=>i.value).join('');
  if(otp.length<6){toast('Enter all 6 digits','','!');return;}
  setLoading('otp-btn',true);
  setTimeout(()=>{
    setLoading('otp-btn',false);
    toast('Verified','Welcome to DevDrop!','◈');
    setTimeout(()=>window.location.href='index.html',900);
  },1300);
}
function resendOtp(){
  toast('Code resent','A new code was sent to your email.','◎');
  document.querySelectorAll('.otp-input').forEach(i=>{i.value='';});
  document.querySelector('.otp-input').focus();
}

/* ════════════════════════════════════
   PASSWORD STRENGTH
════════════════════════════════════ */
function checkStrength(pw){
  let s=0;
  if(pw.length>=8)s++;
  if(/[A-Z]/.test(pw)&&/[a-z]/.test(pw))s++;
  if(/\d/.test(pw))s++;
  if(/[^a-zA-Z0-9]/.test(pw))s++;
  const segs=document.querySelectorAll('.strength-seg');
  const hints=['Too short','Weak','Fair','Good','Strong'];
  const cls=['','s1','s2','s3','s4'];
  segs.forEach((seg,i)=>{
    seg.className='strength-seg';
    if(i<s)seg.classList.add(cls[s]);
  });
  document.getElementById('strength-hint').textContent=pw.length?hints[s]:'Use 8+ characters with letters, numbers & symbols';
}

/* ════════════════════════════════════
   UTILS
════════════════════════════════════ */
function togglePw(id,btn){
  const inp=document.getElementById(id);
  const isText=inp.type==='text';
  inp.type=isText?'password':'text';
  btn.textContent=isText?'Show':'Hide';
}
function toggleCheck(label){
  const cb=label.querySelector('.checkbox');
  if(cb)cb.classList.toggle('checked');
}
function setLoading(btnId,on,paneId){
  const btn=btnId?document.getElementById(btnId):null;
  if(btn){btn.classList.toggle('loading',on);btn.disabled=on;}
  // Also dim surrounding pane lightly for account-row clicks
  if(paneId){
    const p=document.getElementById(paneId);
    if(p)p.style.opacity=on?'.6':'';
  }
}
function shake(id){
  const el=document.getElementById(id);
  if(!el)return;
  el.style.animation='none';
  el.offsetHeight;// reflow
  el.style.animation='shake .4s ease';
  setTimeout(()=>el.style.animation='',400);
}
function isValidEmail(e){return/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)}
function capitalize(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function escHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function escAttr(s){return s.replace(/'/g,'&#39;')}

function toast(title,msg,icon='◈'){
  const w=document.getElementById('toasts');
  const t=document.createElement('div');
  t.className='toast';
  t.innerHTML=`<span class="toast-icon">${icon}</span><div class="toast-body"><div class="toast-title">${title}</div>${msg?`<div class="toast-msg">${msg}</div>`:''}</div>`;
  w.appendChild(t);
  setTimeout(()=>{t.style.transition='opacity .3s,transform .3s';t.style.opacity='0';t.style.transform='translateX(10px)';setTimeout(()=>t.remove(),320);},3500);
}

/* Shake keyframe injected */
const style=document.createElement('style');
style.textContent=`@keyframes shake{0%,100%{transform:translateX(0)}20%,60%{transform:translateX(-5px)}40%,80%{transform:translateX(5px)}}`;
document.head.appendChild(style);

/* ════════════════════════════════════
   INIT
════════════════════════════════════ */
renderAccounts();
renderEmailDropdown('');
// Auto-fill email from URL param e.g. ?email=...
(()=>{
  const p=new URLSearchParams(location.search);
  const e=p.get('email');
  if(e){document.getElementById('login-email').value=e;showPane('pane-login');}
})();