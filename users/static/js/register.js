/**
 * Author: Justin Clayton
 */

'use strict';
(function() {
  $(document).ready(init);

  /** Initialize the JS to control page behavior */
  function init() {
    $('#id_password2').on('input', onCheckPW);
    $('#id_first_name, #id_last_name').on('input', onCheckName)
    $('#id_alias').on('input', onCheckAlias);
  }

  /** Validate that pws match before sending to registration. */
  function onCheckPW() {
    if ($(this).val() === $('#id_password2').val()) {
      this.setCustomValidity('');
    } else {
      this.setCustomValidity('Passwords must match.');
    }
  }

  /** Validates name fields */
  function onCheckName() {
    let re = new RegExp('^[a-zA-Z]{4,45}')
    if (re.test($(this).val())) {
      this.setCustomValidity('')
    } else {
      this.setCustomValidity('Name must be between 4 and 45 characters.')
    }
  }

  /** Check if alias is available */
  function onCheckAlias() {
    if ($(this).val().length > 0) {
      $.get(`/users/check-alias/${$(this).val()}`)
      .done((data) => {
        if ($('#alias-valid').length > 0) {
          $('#alias-valid').removeClass('text-success');
          $('#alias-valid').removeClass('text-danger');
        } else {
          const p = document.createElement('p');
          $(p).attr('id', 'alias-valid');
          $('form p:nth-child(3)').prepend(p);
        }
        if (data === 'available') {
          this.setCustomValidity('')
          $('#alias-valid').text('Alias is available');
          $('#alias-valid').addClass('text-success');
        } else {
          this.setCustomValidity('Alias unavailable please choose another.')
          $('#alias-valid').text('Alias is unavailable');
          $('#alias-valid').addClass('text-danger');
        }
      });
    }
  }
})();
