// Uses Fetch API to pull data and Chart.js to plot it
async function fetchJSON(url, opts={}) {
    const r = await fetch(url, {...opts, credentials: "include"});
    if (!r.ok) throw new Error(await r.text());
    return r.json();
}

// Quick auto-login to demo user so the page “just works”
async function loginDemo() {
    await fetchJSON("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email: "demo@demo.io", password: "demo123"})
    });
}

function makeChart(ctx, label, labels, data, type="line") {
    return new Chart(ctx, {
        type,
        data: {
            labels,
            datasets: [{
                label,
                data,
                borderWidth: 1,
                fill: false
            }]
        }
    });
}

(async () => {
    await loginDemo();
    const expenses = await fetchJSON("/api/expenses");

    // Chart 1: daily spend
    const daily = {};
    expenses.forEach(e=>{
        daily[e.date] = (daily[e.date]||0) + e.amount;
    });
    makeChart(document.getElementById("dailyChart"),
              "Daily Spend",
              Object.keys(daily),
              Object.values(daily));

    // Chart 2: category split
    const cat = {};
    expenses.forEach(e=>{
        cat[e.category] = (cat[e.category]||0)+ e.amount;
    });
    makeChart(document.getElementById("categoryChart"),
              "By Category",
              Object.keys(cat),
              Object.values(cat),
              "bar");

    // Chart 3: forecast
    const forecast = await fetchJSON("/api/forecast");
    makeChart(document.getElementById("forecastChart"),
              "30-day Forecast",
              forecast.map(x=>x.date.slice(0,10)),
              forecast.map(x=>x.prediction));
})();
