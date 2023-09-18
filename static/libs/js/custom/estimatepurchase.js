$(document).ready(function () {
  var $loading = $('#overlay').hide();
  $(document)
  .ajaxStart(function () {
    $loading.show();
  })
  .ajaxStop(function () {
    $loading.hide();
  })
  
  var product_data = []

    $('.supplier_estimate').on("change", function() {
      $.ajax({
          type : "GET",
          url: $('.supplier_product').attr('data-href'),
          data : {'supplier_name': $('#supplier_estimate').val()},
          success : function (data) {
              product_data = data
              $('#prod0').html('<option value="-1">-----------------Select Product-----------------</option>');

              // Add new options based on the data
              for (var i = 0; i < data.Product_data.length; i++) {
                  $('#prod0').append('<option value="' + data.Product_data[i].product_name + '">' + data.Product_data[i].product_name + '</option>');
              }
          }
      })
  });

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
              no=counter+1
              unit='pcs'

              $.ajax({
                type:"GET",
                url: $('#purchase_product_count').attr('data-href'),
                data:{'estimate_purchase_product_count':counter},
                success: function(response){
                  console.log(response)
                },
                error: function(response){
                  alert("error c")
                }
              })

              var newRow= $(document.createElement('tr'))
              .attr("id", 'row' + counter)
              .attr("itemid", counter)
              newRow.html('<td><a id="del'+counter+'" href="#"> <i class="fa fa-trash" style="color: red;"aria-hidden="true"></i> </a></td><td><select name="prod'+counter+'" id="prod'+counter+'" placeholder="Select Product" class="product-select form-control" ><option selected>-----------------Select Product-----------------</option></select></td><td><input type="text" class="tot form-control" id="unit'+ counter +'" name="unit'+ counter +'" readonly ></td><td><input type="number" min="0" step="any" class="form-control" id="rate'+counter+'" name="rate'+counter+'"></td><td><input type="number" min="0" class="addbtntext'+counter+' form-control" id="qty'+counter+'" name="qty'+counter+'"></td><td><input type="number" min="0" step="any" class="form-control" id="dis'+counter+'" name="dis'+counter+'"></td><td><input type="number" class="form-control" id="nr'+counter+'" name="nr'+counter+'"readonly  ></td><td><input type="text" class="tot form-control" id="tot'+counter+'" name="tot'+counter+'" readonly ></td>')
              newRow.appendTo('#itemtable')
  
              $('.product-select').select2();
                for(var i=0;i<product_data.Product_data.length;i++){
                  $('#prod'+counter).append('<option value="'+product_data.Product_data[i].product_name+'">'+product_data.Product_data[i].product_name+'</option>')
                }

          }
      });

      $('#prod'+counter).change(function(){
        var pname=$('#prod'+counter).val()
        var sname = $('#supplier_estimate').val()

        $.ajax({
          type:"GET",
          url: $('.purchaseprice').attr('data-href'),
          data:{'pname':pname , 'sname':sname},
          success: function(response){
            console.log(response)
            $('#rate'+counter).val(response.purchase_price)
            $('#unit'+counter).val(response.product_unit)
            $('#dis'+counter).val(0.0)
          },
          error: function(response){
            console.log("error data not found")
          }
        })

      })

      var id = $(this).closest('tr').attr('itemid');
      $("#rate"+id).keyup(function (){
        var rate=$('#rate'+id).val()
            var dis=$('#dis'+id).val()
            var qty=$('#qty'+id).val()
            var nr=rate-(rate*dis/100)
            $('#nr'+id).val(nr)
            var tot=(nr*qty).toFixed(2)
            $('#tot'+id).val(tot)
            var sum=0;
            $('tr').find('.tot').each(function(){
              if (!isNaN(this.value) && this.value.length != 0) {
                sum += parseFloat(this.value)
              }
            })
            $('#total').val(sum)

           
            
             if($('#roff').keyup(function (){
                var roff=$('#roff').val()
                var total=$('#total').val()
                var oldamt=$('#oldamt').val()
                var gt=parseFloat(total)+parseFloat(oldamt)
                var gtot=gt-parseFloat(roff)
                $('#gtot').val(gtot)
            })){}
            var total=$('#total').val()
              var oldamt=$('#oldamt').val()
              var gt=parseFloat(total)+parseFloat(oldamt)
              $('#gtot').val(gt)

      })

        $('#qty'+id).keyup(function (){
          var rate=$('#rate'+id).val()
            var dis=$('#dis'+id).val()
            var qty=$('#qty'+id).val()
            var nr=rate-(rate*dis/100)
            $('#nr'+id).val(nr)
            var tot=(nr*qty).toFixed(2)
            $('#tot'+id).val(tot)
            var sum=0;
            $('tr').find('.tot').each(function(){
              if (!isNaN(this.value) && this.value.length != 0) {
                sum += parseFloat(this.value)
              }
            })
            $('#total').val(sum)

           
            
             if($('#roff').keyup(function (){
                var roff=$('#roff').val()
                var total=$('#total').val()
                var oldamt=$('#oldamt').val()
                var gt=parseFloat(total)+parseFloat(oldamt)
                var gtot=gt-parseFloat(roff)
                $('#gtot').val(gtot)
            })){}
            var total=$('#total').val()
              var oldamt=$('#oldamt').val()
              var gt=parseFloat(total)+parseFloat(oldamt)
              $('#gtot').val(gt)

        })

          $("#dis" + id).keyup(function(){
        
            var rate=$('#rate'+id).val()
            var dis=$('#dis'+id).val()
            var qty=$('#qty'+id).val()
            var nr=rate-(rate*dis/100)
            $('#nr'+id).val(nr)
            var tot=(nr*qty).toFixed(2)
            $('#tot'+id).val(tot)
            var sum=0;
            $('tr').find('.tot').each(function(){
              if (!isNaN(this.value) && this.value.length != 0) {
                sum += parseFloat(this.value)
              }
            })
            $('#total').val(sum)

           
            
             if($('#roff').keyup(function (){
                var roff=$('#roff').val()
                var total=$('#total').val()
                var oldamt=$('#oldamt').val()
                var gt=parseFloat(total)+parseFloat(oldamt)
                var gtot=gt-parseFloat(roff)
                $('#gtot').val(gtot)
            })){}
            var total=$('#total').val()
              var oldamt=$('#oldamt').val()
              var gt=parseFloat(total)+parseFloat(oldamt)
              $('#gtot').val(gt)
        })

      $('#del'+counter).click(function (){
          if ($('#row'+counter).attr('itemid') == 0){
          }
          else {
            var sum=0;
            $('tr').find('.tot').each(function(){
              if (!isNaN(this.value) && this.value.length != 0) {
                sum += parseFloat(this.value)
              }
            })
            $('#total').val(sum)
            $('#row'+counter).remove()
            var total=$('#total').val()
            var oldamt=$('#oldamt').val()
            var gt=parseFloat(total)+parseFloat(oldamt)
            $('#gtot').val(gt)
        }
      })
      
  });
});
