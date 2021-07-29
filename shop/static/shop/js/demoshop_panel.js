let cookie = 'hide_insales_panel'
let html = document.querySelector('html');

let togglePanel = (show) => {
  let method = show ? 'remove' : 'add'
  html.classList[method]('hide-insales-panel');
}

let loadJSONP = (() => {
  let unique = 0;
  return function(url, callback, context) {
    let name = "_jsonp_" + unique++;
    if (url.match(/\?/)) {
      url += "&callback=" + name;
    } else {
      url += "?callback=" + name;
    }

    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;

    window[name] = function(data) {
      callback.call(context || window, data);
      document.getElementsByTagName('head')[0].removeChild(script);
      script = null;
      delete window[name];
    };

    document.getElementsByTagName('head')[0].appendChild(script);
  };
})();

let initDemoShopButton = () => {
  if (document.querySelector('[data-demoshop-auth]')) {
    let authUrl = document.querySelector('[data-demoshop-auth]').dataset.demoshopAuth
    loadJSONP(authUrl, (response) => { drawDemoShopButton(response); })
  }
}

let drawDemoShopButton = (data) => {
  if (!data.domains || data.domains.length == 0) {
    document.querySelector('#demo-create-shop').style.display = 'block'
    return
  }

  let firstDomain = data.domains[0]
  let demoUseTheme = document.querySelector('#demo-use-theme')
  let demoUseThemeLink = demoUseTheme.querySelector('a')

  demoUseThemeLink.href = `${firstDomain.url}${demoUseThemeLink.getAttribute("href")}`
  demoUseThemeLink.innerHTML = `${demoUseThemeLink.innerHTML} для ${firstDomain.domain}`

  demoUseTheme.style.display = 'block'
}

togglePanel(!~document.cookie.indexOf(`${cookie}=true`))

window.addEventListener('load', () => {
  document.querySelector('.insales-panel .inner-toggle-panel').addEventListener('click', function() {
    let show = html.classList.contains('hide-insales-panel');
    togglePanel(show)
    document.cookie = `${cookie}=${!show || ''};path=/`;
  })

  initDemoShopButton()
});
