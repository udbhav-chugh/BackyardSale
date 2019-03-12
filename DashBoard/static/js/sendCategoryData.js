$("#id_Category").change(function () {
        const url = $("#itemForm").attr("data-subCat-url");  // get the url of the `load_subCats` view
        const Category = $(this).val();  // get the selected Category ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/dashboard/ajax/load-subCats/)
        data: {
          'Category': Category       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `getSubCategories` view function
          $("#id_SubCategory").html(data);  // replace the contents of the SubCategory input with the data that came from the server
        }
      });

    });