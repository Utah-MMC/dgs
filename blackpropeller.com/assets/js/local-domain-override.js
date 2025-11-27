/**
 * When browsing the static export locally (localhost/127.0.0.1),
 * force internal links that still point at the production origin
 * to resolve against the local server instead.
 */
(function () {
  var LOCAL_HOST_PATTERN = /^(localhost|127\.0\.0\.1)(:\d+)?$/;
  if (!LOCAL_HOST_PATTERN.test(window.location.host)) {
    return;
  }

  var PROD_HOST = "digitalgrowthstudios.com";
  var PROD_HTTP = "http://" + PROD_HOST;
  var PROD_HTTPS = "https://" + PROD_HOST;
  var PROD_PROTOCOL_REL = "//" + PROD_HOST;

  function normalizePath(url) {
    if (!url) return url;

    if (url.startsWith(PROD_HTTPS)) {
      return url.substring(PROD_HTTPS.length) || "/";
    }

    if (url.startsWith(PROD_HTTP)) {
      return url.substring(PROD_HTTP.length) || "/";
    }

    if (url.startsWith(PROD_PROTOCOL_REL)) {
      return url.substring(PROD_PROTOCOL_REL.length) || "/";
    }

    return null;
  }

  function rewriteAttribute(node, attr) {
    var current = node.getAttribute(attr);
    var replacement = normalizePath(current);
    if (replacement === null) return;
    if (replacement && replacement.charAt(0) !== "/") {
      replacement = "/" + replacement;
    }
    node.setAttribute(attr, replacement || "/");
  }

  var selectors = [
    ["a", "href"],
    ["link", "href"],
    ["form", "action"],
    ["script", "src"]
  ];

  selectors.forEach(function (pair) {
    var elements = document.querySelectorAll(pair[0] + "[" + pair[1] + "]");
    elements.forEach(function (el) {
      rewriteAttribute(el, pair[1]);
    });
  });
})();

