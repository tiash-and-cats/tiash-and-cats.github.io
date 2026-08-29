class FacebookAccountCountdown extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });

    this.shadowRoot.innerHTML = `
      <style>
        .fbcount {
          background-image: linear-gradient(#0064e0, #1877f2);
          position: relative;
          color: white;
          font-family: facebook, Segoe UI Historic, Segoe UI, Helvetica, Arial, sans-serif;
          font-size: 1.5625rem;
          padding: 1em;
          padding-bottom: 1.5em;
        }
        
        .fbcount p {
          margin-block: 0.5em;
        }

        .fbcount .countdown {
          font-size: 1.2em;
        }

        .fbcount h1 {
          margin-bottom: 0.25em;
        }
      </style>
      <div class="fbcount">
        <h1>Countdown until I can get a new Facebook account</h1>
        <p class="countdown"></p>
        <p>My old one got terminated for being underage. I just used to use it for Messenger. Not too sad about it, as I was, in fact, underage, and I didn't use Facebook much anyway.</p>
        <p>This counts down until my 13th birthday, which, as I live in Bangladesh, is the age that I can officially open a Facebook account.</p>
        <p>That's why you can't reach me on Messenger. Don't worry, I'm still alive!</p>
      </div>
    `;
  }

  connectedCallback() {
    // September 22, 2027, at 8:20 AM, BDST
    const countDownDate = new Date("2027-09-22T08:20:00+06:00").getTime();
    const countdownEl = this.shadowRoot.querySelector(".countdown");

    function updateCountdown() {
      const now = new Date().getTime();
      const distance = countDownDate - now;

      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);

      if (countdownEl) {
        countdownEl.textContent = distance > 0
          ? `${days}d ${hours}h ${minutes}m ${seconds}s`
          : "Yay! I can make one now.";
      }
    }

    updateCountdown();
    this._interval = setInterval(updateCountdown, 1000);
  }

  disconnectedCallback() {
    clearInterval(this._interval);
  }
}

class MyAge extends HTMLElement {
  connectedCallback() {
    const birthDate = new Date("2014-09-22T08:20:00+06:00");
    const today = new Date();

    let age = today.getFullYear() - birthDate.getFullYear();
    const hasHadBirthdayThisYear =
      today.getMonth() > birthDate.getMonth() ||
      (today.getMonth() === birthDate.getMonth() &&
       today.getDate() >= birthDate.getDate());

    if (!hasHadBirthdayThisYear) {
      age--;
    }
    
    this.textContent = age;
  }
}

customElements.define("fb-acc-countdown", FacebookAccountCountdown);
customElements.define("my-age", MyAge);