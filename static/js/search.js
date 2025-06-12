$(document).ready(function () {
  $("#Csearch").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#client_table #client_name").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).ready(function () {
  $("#Msearch").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#medicine_table #medicine_name").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).ready(function () {
  $("#Psearch").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".payment-box #payment_info").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).ready(function () {
  $("#Prescription_search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".prescription-box .prescription-details").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});