// Load header and footer includes
(function() {
  'use strict';
  
  // Function to load and inject HTML
  function loadInclude(elementId, filePath) {
    const element = document.getElementById(elementId);
    if (!element) {
      console.warn('Element with id "' + elementId + '" not found');
      return;
    }
    
    fetch(filePath)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to load ' + filePath + ': ' + response.status);
        }
        return response.text();
      })
      .then(html => {
        element.innerHTML = html;
        // Execute any scripts in the loaded HTML
        const scripts = element.querySelectorAll('script');
        scripts.forEach(oldScript => {
          const newScript = document.createElement('script');
          Array.from(oldScript.attributes).forEach(attr => {
            newScript.setAttribute(attr.name, attr.value);
          });
          newScript.appendChild(document.createTextNode(oldScript.innerHTML));
          oldScript.parentNode.replaceChild(newScript, oldScript);
        });
      })
      .catch(error => {
        console.error('Error loading include:', error);
      });
  }
  
  // Load includes when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      loadInclude('site-header', '/includes/header.html');
      loadInclude('site-footer', '/includes/footer.html');
    });
  } else {
    loadInclude('site-header', '/includes/header.html');
    loadInclude('site-footer', '/includes/footer.html');
  }
})();

