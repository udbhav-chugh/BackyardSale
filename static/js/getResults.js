$("#search").keyup(function () {
      $.ajax({
        type: 'POST',
        url: 'search/',                    // set the url of the request (= localhost:8000/dashboard/ajax/load-subCats/)
        data: {
          'search_text': $("#search").val(),
          'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function (data) {   // `data` is the return of the `getSubCategories` view function
          $("#search-results").html(data);  // replace the contents of the SubCategory input with the data that came from the server
        }
      });

    });