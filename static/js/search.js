$(document).ready(function () {
  $("#medicine-search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#medicine-table #medicine-name").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).ready(function () {
  $("#disease-search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#disease-table #disease-name").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).ready(function () {
  $("#transaction-search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".transaction-box .transaction-container").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).ready(function () {
  $("#prescription-search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".prescription-box .prescription-container").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).ready(function () {
  $("#diagnosis-search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".diagnosis-box .diagnosis-container").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).ready(function () {
  $("#labtest-search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".labtest-box .diagnosis-container").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});
