$(document).ready(function () {
  var $loading = $('#overlay').hide();
  $(document)
    .ajaxStart(function () {
      $loading.show();
    })
    .ajaxStop(function () {
      $loading.hide();
    });

  var product_data = []
  var supplier_state;

  $('.supplier_gst').on("change", function() {
    $.ajax({
        type : "GET",
        url: $('.supplier_product').attr('data-href'),
        data : {'supplier_name': $('#supplier_gst').val()},
        success : function (data) {
          console.log(data)
            product_data = data
            $('#prod0').html('<option value="-1">-----------------Select Product-----------------</option>');

            // Add new options based on the data
            for (var i = 0; i < data.Product_data.length; i++) {
                $('#prod0').append('<option value="' + data.Product_data[i].product_name + '">' + data.Product_data[i].product_name + '</option>');
            }
            supplier_state = data.supplier_state
        }
    })
});

  var profile_state = $('#owner_state').val();

  var counter = 1;
  $(document).on('focus', "tr td", function (e) {

    myString = $(this).closest('tr').attr('itemid');
    counter = myString;

    var prnt = $(this).closest('tr').attr('itemid');

    var lst = Number(prnt) + Number(1);

    $(".addbtntext" + counter).focus(function () {
      if (document.getElementById("row" + lst) != null) {

      } else {
        counter++;
        no = counter + 1

        $('#product_count').val(counter)

        var newRow = $(document.createElement('tr'))
          .attr("id", 'row' + counter)
          .attr("itemid", counter)
        newRow.html('<td><a id="del' + counter + '" href="#"> <i class="fa fa-trash" style="color: red;"aria-hidden="true"></i> </a></td><td><input type="number" min="0" class="form-control" id="hsn' + counter + '" name="hsn' + counter + '"></td><td><select name="prod' + counter + '" id="prod' + counter + '" placeholder="Select Product" class="product-select form-control" ><option selected>--------Select Product--------</option></select></td><td><input type="text" class="tot form-control" id="unit' + counter + '" name="unit' + counter + '" readonly ></td><td><input type="number" min="0" step="any" class="form-control" id="rate' + counter + '" name="rate' + counter + '"></td><td><input type="number" min="0" class="form-control" id="qty' + counter + '" name="qty' + counter + '"></td><td><input type="number" min="0" step="any" class="addbtntext' + counter + ' form-control" id="gstp' + counter + '" name="gstp' + counter + '"></td><td><input type="number" class="gstamt form-control" id="gstamt' + counter + '" name="gstamt' + counter + '"readonly  ></td><td><input type="text" class="tot form-control" id="tot' + counter + '" name="tot' + counter + '" readonly ></td>')
        newRow.appendTo('#itemtable')

        $('.product-select').select2();
        for (var i = 0; i < product_data.Product_data.length; i++) {
          $('#prod' + counter).append('<option value="' + product_data.Product_data[i].product_name + '">' + product_data.Product_data[i].product_name + '</option>')
        }
      }
    });

    $('#prod' + counter).change(function () {
      var pname = $('#prod' + counter).val()

      $.ajax({
        type: "GET",
        url: $('.purchaseprice').attr('data-href'),
        data: { 'pname': pname},
        success: function (response) {
          $('#rate' + counter).val(response.purchase_price)
          $('#unit' + counter).val(response.product_unit)
        },
        error: function (response) {
          console.log("error data not found")
        }
      })
    });

      var id = $(this).closest('tr').attr('itemid');
      $("#rate" + id).keyup(function () {
        var rate = $('#rate' + id).val()
        var qty = $('#qty' + id).val()
        var gstp = $('#gstp' + id).val()

        var tot = parseFloat(rate) * parseFloat(qty)
        var gstamt = tot * gstp / 100
        $('#gstamt' + id).val(gstamt)
        $('#tot' + id).val(tot)

        var sum = 0;
        $('tr').find('.tot').each(function () {
          if (!isNaN(this.value) && this.value.length != 0) {
            sum += parseFloat(this.value)
          }
        })
        $('#total').val(sum)
        if (supplier_state === profile_state) {
          var gstsum = 0;
          $('tr').find('.gstamt').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              gstsum = (parseFloat(this.value) + parseFloat(gstsum)).toFixed(2)
            }
          })
          var cgst = gstsum / 2
          $('#cgst').val(cgst)
          $('#sgst').val(cgst)
        }
        else {
          var gstsum = 0;
          $('tr').find('.gstamt').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              gstsum = (parseFloat(this.value) + parseFloat(gstsum)).toFixed(2)
            }
          })
          $('#igst').val(gstsum)
        }

        if ($('#roff').keyup(function () {
          var gsts = 0;
          $('tr').find('.gstamt').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              gsts += parseFloat(this.value)
            } 
          })
          var roff = $('#roff').val()
          var total = $('#total').val()
          var gt = parseFloat(total) + gsts
          var gtot = gt - parseFloat(roff)
          $('#gtot').val(gtot)
        })) { }
        var total = $('#total').val()
        var gt = parseFloat(total) + parseFloat(gstsum)
        $('#gtot').val(gt)
      })

      $('#qty' + id).keyup(function () {
        var rate = $('#rate' + id).val()
        var qty = $('#qty' + id).val()
        var gstp = $('#gstp' + id).val()

        var tot = parseFloat(rate) * parseFloat(qty)
        var gstamt = tot * gstp / 100
        $('#gstamt' + id).val(gstamt)
        $('#tot' + id).val(tot)

        var sum = 0;
        $('tr').find('.tot').each(function () {
          if (!isNaN(this.value) && this.value.length != 0) {
            sum += parseFloat(this.value)
          }
        })
        $('#total').val(sum)
        if (supplier_state === profile_state) {
          var gstsum = 0;
          $('tr').find('.gstamt').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              gstsum = (parseFloat(this.value) + parseFloat(gstsum)).toFixed(2)
            }
          })
          var cgst = gstsum / 2
          $('#cgst').val(cgst)
          $('#sgst').val(cgst)
        }
        else {
          var gstsum = 0;
          $('tr').find('.gstamt').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              gstsum = (parseFloat(this.value) + parseFloat(gstsum)).toFixed(2)
            }
          })
          $('#igst').val(gstsum)
        }

        if ($('#roff').keyup(function () {
          var gsts = 0;
          $('tr').find('.gstamt').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              gsts += parseFloat(this.value)
            }
          })
          var roff = $('#roff').val()
          var total = $('#total').val()
          var gt = parseFloat(total) + gsts
          var gtot = gt - parseFloat(roff)
          $('#gtot').val(gtot)
        })) { }
        var total = $('#total').val()
        var gt = parseFloat(total) + parseFloat(gstsum)
        $('#gtot').val(gt)

      })

      $(".addbtntext" + id).keyup(function () {

        var rate = $('#rate' + id).val()
        var qty = $('#qty' + id).val()
        var gstp = $('#gstp' + id).val()

        var tot = parseFloat(rate) * parseFloat(qty)
        var gstamt = tot * gstp / 100
        $('#gstamt' + id).val(gstamt)
        $('#tot' + id).val(tot)

        var sum = 0;
        $('tr').find('.tot').each(function () {
          if (!isNaN(this.value) && this.value.length != 0) {
            sum += parseFloat(this.value)
          }
        })
        $('#total').val(sum)

        if (supplier_state === profile_state) {
          var gstsum = 0;
          $('tr').find('.gstamt').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              gstsum = (parseFloat(this.value) + parseFloat(gstsum)).toFixed(2)
            }
          })
          var cgst = gstsum / 2
          $('#cgst').val(cgst)
          $('#sgst').val(cgst)
        }
        else {
          var gstsum = 0;
          $('tr').find('.gstamt').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              gstsum = (parseFloat(this.value) + parseFloat(gstsum)).toFixed(2)
            }
          })
          $('#igst').val(gstsum)
        }

        if ($('#roff').keyup(function () {
          var gsts = 0;
          $('tr').find('.gstamt').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              gsts += parseFloat(this.value)
            }
          })
          var roff = $('#roff').val()
          var total = $('#total').val()
          var gt = parseFloat(total) + gsts
          var gtot = gt - parseFloat(roff)
          $('#gtot').val(gtot)
        })) { }
        var total = $('#total').val()
        var gt = parseFloat(total) + parseFloat(gstsum)
        $('#gtot').val(gt)

      })

      $('#del' + counter).click(function () {
        if ($('#row' + counter).attr('itemid') == 0) {
        }
        else {
          var sum = 0;
          $('tr').find('.tot').each(function () {
            if (!isNaN(this.value) && this.value.length != 0) {
              sum += parseFloat(this.value)
            }
          })
          // gst calculate
          if (supplier_state == profile_state) {
            var gstsum = 0;
            $('tr').find('.gstamt').each(function () {
              if (!isNaN(this.value) && this.value.length != 0) {
                gstsum += parseFloat(this.value)
              }
            })
            var cgst = gstsum / 2
            $('#cgst').val(cgst)
            $('#sgst').val(cgst)
          }
          else {
            var gstsum = 0;
            $('tr').find('.gstamt').each(function () {
              if (!isNaN(this.value) && this.value.length != 0) {
                gstsum += parseFloat(this.value)
              }
            })
            $('#igst').val(gstsum)
          }
          // end gst calculate 
  
          $('#total').val(sum)
          $('#row' + counter).remove()
          var total = $('#total').val()
          var roff = $('#roff').val()
          var gt = parseFloat(total) + parseFloat(gstsum) - parseFloat(roff)
          $('#gtot').val(gt)
        }
      })
    });
});