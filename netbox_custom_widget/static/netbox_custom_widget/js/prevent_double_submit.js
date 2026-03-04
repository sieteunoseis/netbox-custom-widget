// Toggle visibility of the category filter field based on the endpoint selection.
// Only show it when "bookmarks" is selected.
(function() {
  function toggleCategoryField(modal) {
    var endpoint = modal.querySelector('[name="endpoint_id"]');
    var categoryField = modal.querySelector('[name="category"]');
    if (!endpoint || !categoryField) return;
    var row = categoryField.closest('.mb-3') || categoryField.closest('.form-group') || categoryField.parentElement;
    if (!row) return;
    if (endpoint.value === 'bookmarks') {
      row.style.display = '';
    } else {
      row.style.display = 'none';
      categoryField.value = '';
    }
  }

  // Watch for modals being populated (HTMX swaps content into modals)
  document.body.addEventListener('htmx:afterSettle', function(e) {
    var modal = e.target.closest('.modal') || e.target.querySelector('.modal');
    if (!modal) modal = document.querySelector('.modal.show');
    if (!modal) return;
    var endpoint = modal.querySelector('[name="endpoint_id"]');
    if (!endpoint) return;
    toggleCategoryField(modal);
    endpoint.addEventListener('change', function() {
      toggleCategoryField(modal);
    });
  });
})();

// Prevent double-submission on dashboard widget config forms.
// NetBox uses HTMX (hx-post) for widget add/config forms, so we hook
// into htmx:beforeRequest instead of the native submit event.
(function() {
  document.body.addEventListener('htmx:beforeRequest', function(e) {
    const form = e.detail.elt;
    if (form.tagName !== 'FORM') return;
    // Only target dashboard widget forms
    if (!form.closest('.modal')) return;
    if (!form.querySelector('[name="widget_class"]') && !form.hasAttribute('hx-post')) return;

    const btn = form.querySelector('.modal-footer .btn-primary');
    if (!btn) return;

    if (btn.disabled) {
      // Already in flight — cancel the duplicate request
      e.preventDefault();
      return;
    }

    btn.disabled = true;
    btn.dataset.originalText = btn.innerHTML;
    btn.innerHTML = '<i class="mdi mdi-loading mdi-spin"></i> Saving...';
  });

  // Re-enable on completion (success or error)
  document.body.addEventListener('htmx:afterRequest', function(e) {
    const form = e.detail.elt;
    if (form.tagName !== 'FORM' || !form.closest('.modal')) return;

    const btn = form.querySelector('.modal-footer .btn-primary');
    if (btn && btn.dataset.originalText) {
      btn.disabled = false;
      btn.innerHTML = btn.dataset.originalText;
    }
  });
})();
