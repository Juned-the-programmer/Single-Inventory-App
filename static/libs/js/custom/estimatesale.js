$(document).ready(function () {
  var $loading = $('#overlay').hide();
  $(document)
  .ajaxStart(function () {
    $loading.show();
  })
  .ajaxStop(function () {
    $loading.hide();
  });

  var product_data =[]
    $.ajax({
      type:"GET",
      url: $('.product_data_estimate').attr('data-href'),
      async : false,
      success: function(response){
        product_data = response
      },
    })

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
                url: $('#c').attr('data-href'),
                data:{'c':counter},
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
                for(var i=0;i<product_data.productdata.length;i++){
                  $('#prod'+counter).append('<option value="'+product_data.productdata[i].product_name+'">'+product_data.productdata[i].product_name+'</option>')
                }

          }
      });

      $('#prod'+counter).change(function(){
        var pname=$('#prod'+counter).val()
    
        $('#dis'+counter).val(0.0)

        $.ajax({
          type: "GET",
          url : $('.selected_product').attr('data-href'),
          data : {'product_name' : pname},
          success : function(data) {
            var product_data = data.product_data
            $('#unit'+counter).val(product_data.product_unit)
            $('#rate'+counter).val(parseFloat(product_data.rate))
            if(product_data.quantity == 0){
              $('#qty'+counter).prop('disabled',true)
              alert("you don't have enough stock")
            } else {
              $('#qty'+counter).prop('disabled',false)
              $('#qty'+counter).attr('max', product_data.quantity)
            }
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
            var roff=$('#roff').val()
            var gt=parseFloat(total)+parseFloat(oldamt)-parseFloat(roff)
            $('#gtot').val(gt)
        }
      })
      
  });
});
