class FbCount extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });

    this.shadowRoot.innerHTML = `
      <style>
        @font-face {
          font-family: 'facebook';
          src: url('/assets/fonts/facebook.woff2') format('woff2');
          font-weight: normal;
          font-style: normal;
          font-display: swap;
        }

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
        <h1><slot name="title">Countdown until I can get a new Facebook account</slot></h1>
        <p class="countdown"></p>
        <p><slot name="description">My old one got terminated for being underage. I just used to use it for Messenger. Not too sad about it, as I was underage and I didn't use Facebook much.</slot></p>
      </div>
    `;
  }

  connectedCallback() {
    const countDownDate = new Date("Sep 22, 2027 8:20:00").getTime();
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

customElements.define("fb-count", FbCount);