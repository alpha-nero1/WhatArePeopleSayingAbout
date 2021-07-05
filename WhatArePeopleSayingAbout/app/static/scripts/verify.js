function recaptchaCallback() {
    // Listen on recaptcha.
    const btn = document.getElementById('captcha-blocked-button')
    if (!btn) return;
    btn.disabled = false;
}
