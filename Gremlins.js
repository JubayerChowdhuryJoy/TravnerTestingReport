(async function() {
  // -----------------------------
  // 1️⃣ Load dependencies
  // -----------------------------
  async function loadScript(url) {
    return new Promise(resolve => {
      const s = document.createElement('script');
      s.src = url;
      s.onload = resolve;
      document.head.appendChild(s);
    });
  }

  await loadScript('https://unpkg.com/gremlins.js');
  await loadScript('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js');
  await loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');

  // -----------------------------
  // 2️⃣ Setup report
  // -----------------------------
  const monkeyReport = {
    errors: [],
    consoleLogs: [],
    visitedUrls: new Set(),
    screenshots: []
  };

  // -----------------------------
  // 3️⃣ Capture JS errors
  // -----------------------------
  window.addEventListener('error', e => {
    monkeyReport.errors.push({
      type: 'error',
      message: e.message,
      filename: e.filename,
      lineno: e.lineno,
      colno: e.colno,
      time: new Date().toISOString(),
      url: window.location.href
    });
    console.error("Monkey Test Error:", e.message);
  });

  // -----------------------------
  // 4️⃣ Capture console logs
  // -----------------------------
  ['log','warn','error','info'].forEach(method => {
    const original = console[method];
    console[method] = function(...args) {
      const message = args.map(a => (typeof a==='object'?JSON.stringify(a):a)).join(' ');
      if(message.includes("Production environment detected")) return;
      monkeyReport.consoleLogs.push({ type: method, message, time: new Date().toISOString(), url: window.location.href });
      original.apply(console, args);
    };
  });

  // -----------------------------
  // 5️⃣ Wait for dynamic elements
  // -----------------------------
  function waitForSelector(selector, timeout = 5000) {
    return new Promise(resolve => {
      const interval = setInterval(() => {
        if(document.querySelector(selector)) { clearInterval(interval); resolve(true); }
      }, 100);
      setTimeout(() => { clearInterval(interval); resolve(false); }, timeout);
    });
  }

  // -----------------------------
  // 6️⃣ Pre-fill Sign Up/Login forms
  // -----------------------------
  async function fillForms() {
    const formExists = await waitForSelector('form');
    if(!formExists) return;
    document.querySelectorAll('form').forEach(form => {
      form.querySelectorAll('input').forEach(input => {
        if(input.type==='email') input.value='test@example.com';
        else if(input.type==='password') input.value='Password123';
        else input.value='Test';
      });
    });
  }

  await fillForms();

  // -----------------------------
  // 7️⃣ Screenshot function
  // -----------------------------
  async function captureScreenshot() {
    const canvas = await html2canvas(document.body);
    const dataURL = canvas.toDataURL();
    monkeyReport.screenshots.push({ time: new Date().toISOString(), url: window.location.href, dataURL });
    console.log(`Screenshot captured at ${window.location.href}`);
  }

  // -----------------------------
  // 8️⃣ Navigation
  // -----------------------------
  function getInternalLinks() {
    return Array.from(document.querySelectorAll('a[href^="/"]'))
      .map(a => a.href)
      .filter((v,i,a) => a.indexOf(v) === i);
  }

  function navigateRandom() {
    const links = getInternalLinks().filter(url => !monkeyReport.visitedUrls.has(url));
    if (!links.length) return;
    const nextUrl = links[Math.floor(Math.random() * links.length)];
    console.log("Navigating to:", nextUrl);
    monkeyReport.visitedUrls.add(nextUrl);
    window.location.href = nextUrl;
  }

  // -----------------------------
  // 9️⃣ Detect and interact with dynamic elements
  // -----------------------------
  function interactWithDynamicElements() {
    // Click all visible buttons
    document.querySelectorAll('button, input[type="button"], input[type="submit"]').forEach(btn => {
      if(btn.offsetParent !== null) btn.click();
    });
    // Type into visible text/textarea inputs
    document.querySelectorAll('input[type="text"], input[type="email"], textarea').forEach(input => {
      if(input.offsetParent !== null) input.value = input.value || 'Test';
    });
    // Scroll randomly
    window.scrollTo(0, Math.random() * document.body.scrollHeight);
  }

  // -----------------------------
  //  🔟 Start Gremlins horde
  // -----------------------------
  const duration = 120000; // 2 minutes
  console.log("Starting SPA + Dynamic Content Monkey Test for", duration/1000, "seconds");

  monkeyReport.visitedUrls.add(window.location.href);

  const horde = gremlins.createHorde({
    species: [
      gremlins.species.clicker(),
      gremlins.species.formFiller(),
      gremlins.species.typer({ allAtOnce: false }),
      gremlins.species.scroller()
    ],
    strategies: [gremlins.strategies.distribution({ delay: 100 })]
  });

  // Screenshots every 15s
  const screenshotInterval = setInterval(captureScreenshot, 15000);
  // Navigate internal pages every 20s
  const navInterval = setInterval(navigateRandom, 20000);
  // Interact with dynamic elements every 3s
  const dynamicInterval = setInterval(interactWithDynamicElements, 3000);

  horde.unleash({ duration });

  // -----------------------------
  //  11️⃣ Stop and generate PDF
  // -----------------------------
  setTimeout(async () => {
    clearInterval(screenshotInterval);
    clearInterval(navInterval);
    clearInterval(dynamicInterval);
    console.log("Monkey Test Finished!");

    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF();

    pdf.setFontSize(16);
    pdf.text("Monkey Test Report", 10, 10);
    pdf.setFontSize(12);
    pdf.text(`Test URL: ${window.location.origin}`, 10, 20);
    pdf.text(`Date: ${new Date().toLocaleString()}`, 10, 28);

    let y = 38;

    // Errors
    pdf.setFontSize(14);
    pdf.text("JavaScript Errors:", 10, y); y+=6;
    pdf.setFontSize(10);
    if(monkeyReport.errors.length===0) pdf.text("No JS errors captured.",10,y);
    else monkeyReport.errors.forEach((err,i)=>{
      if(y>270){pdf.addPage(); y=10;}
      pdf.text(`${i+1}. ${err.message} (${err.url}) at ${err.time}`,10,y); y+=6;
    });

    // Console logs
    pdf.addPage(); y=10;
    pdf.setFontSize(14); pdf.text("Console Logs:", 10, y); y+=6;
    pdf.setFontSize(10);
    if(monkeyReport.consoleLogs.length===0) pdf.text("No console logs captured.",10,y);
    else monkeyReport.consoleLogs.forEach((c,i)=>{
      if(y>270){pdf.addPage(); y=10;}
      pdf.text(`${i+1}. [${c.type}] ${c.message} (${c.url}) at ${c.time}`,10,y); y+=6;
    });

    // Screenshots
    pdf.addPage(); y=10;
    pdf.setFontSize(14); pdf.text("Screenshots:",10,y); y+=6;
    for(let i=0;i<monkeyReport.screenshots.length;i++){
      const s=monkeyReport.screenshots[i];
      if(y>250){pdf.addPage(); y=10;}
      pdf.setFontSize(10);
      pdf.text(`Time: ${s.time} URL: ${s.url}`,10,y); y+=6;
      pdf.addImage(s.dataURL,'PNG',10,y,180,100); y+=105;
    }

    pdf.save(`SPA_Dynamic_MonkeyTestReport_${Date.now()}.pdf`);
    console.log("PDF report generated and downloaded.");
    console.log("Final Monkey Report:", monkeyReport);
    alert("Monkey Test Finished! PDF report downloaded. Check console for detailed log.");
  }, duration);

})();
