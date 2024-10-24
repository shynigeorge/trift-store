$(document).ready(function () {
  // Initially hide all forms except the active form
  $('#signup-form, #delivery-form, #login-form').hide();

  // Show the active form on page load after a short delay
  var activeTab = $('.nav-tabs li.active a').attr('href');
  setTimeout(function () {
    $(activeTab + '-form').fadeIn(800);
  }, 100);

  $('.nav-tabs a').on('click', function (e) {
    e.preventDefault();

    // Remove active class from all tabs and hide all forms
    $('.nav-tabs li').removeClass('active');
    $('#signup-form, #delivery-form, #login-form').hide();

    // Add active class to the clicked tab
    $(this).parent().addClass('active');

    // Show the selected form after a short delay
    setTimeout(function () {
      $($(this).attr('href') + '-form').fadeIn(800);
    }.bind(this), 100);
  });

  // The following code is the part you provided for input and label styling
  $('#form').find('input, textarea').on('keyup blur focus', function (e) {
    var $this = $(this),
      label = $this.prev('label');

    if (e.type === 'keyup') {
      if ($this.val() === '') {
        label.removeClass('active highlight');
      } else {
        label.addClass('active highlight');
      }
    } else if (e.type === 'blur') {
      if ($this.val() === '') {
        label.removeClass('active highlight');
      } else {
        label.removeClass('highlight');
      }
    } else if (e.type === 'focus') {
      if ($this.val() === '') {
        label.removeClass('highlight');
      } else if ($this.val() !== '') {
        label.addClass('highlight');
      }
    }
  });
});
