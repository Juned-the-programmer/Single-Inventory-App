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
    var stock = []
    $.ajax({
      type:"GET",
      url: $('.product_data_estimate').attr('data-href'),
      async : false,
      success: function(response){
        product_data = response
      },
    })

    $.ajax({
      type:"GET",
      url: $('.stock_data_estimate').attr('data-href'),
      async : false,
      success: function(response){ 
        stock = response
      },
    })
    console.log(product_data);
    console.log(stock);

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
        var cname=$('#cname').val()
        
        $.ajax({
          type:"GET",
          url: $('.sellingprice_estimate').attr('data-href'),
          data:{'pname':pname , 'cname':cname},
          success: function(response){
            $('#rate'+counter).val(response)
            // alert(response)
          },
          error: function(response){
            console.log("error data not found")
          }
        })
        
        $.ajax({
          type:"GET",
          url: $('.previous_discount_estimate').attr('data-href'),
          data:{'pname':pname , 'cname':cname},
          success: function(response){
            $('#dis'+counter).val(response)
            // alert(response)
          },
          error: function(response){
            console.log("error data not found")
          }
        })

        for(var i=0;i<product_data.productdata.length;i++){
          if(product_data.productdata[i].product_name === pname){
            $('#unit'+counter).val(product_data.productdata[i].unit)
          }
          if(product_data.productdata[i].product_name === pname){
            var id = product_data.productdata[i].id;
            if(stock.stock_data[i].product_id === id){
                var stock_check = stock.stock_data[i]
                if (stock_check.quantity <= 0){
                  $('#qty'+counter).prop('disabled',true)
                  alert("you don't have enough stock")
                }
                else{
                  $('#qty'+counter).prop('disabled',false)
                  $('#qty'+counter).attr('max',stock_check.quantity)
                }
            }
          }
        }


        // $.ajax({
        //   type:"GET",
        //   url: $('.punit').attr('data-href'),
        //   data:{'pname':pname},
        //   success: function(response){
        //     $('#unit'+counter).val(response)
        //   },
        //   error: function(response){
        //     console.log("error not data found")
        //   }
        // })
        
        // $.ajax({
        //   type:"GET",
        //   url: $('#check_stock_estimate').attr('data-href'),
        //   data:{'pname':pname},
        //   success: function(response){
        //     if(response <= 0){
        //       $('#qty'+counter).prop('disabled',true)
        //       alert("you don't have enough stock")
        //     }
        //     else{
        //       $('#qty'+counter).prop('disabled',false)
        //       $('#qty'+counter).attr('max',response)
        //       console.log(response);    
        //     }
        //   }
        // })

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
  
  $('.addsales').Click(function (){
    var c=$('tbody').find('tr:last').attr('itemid')
        $.ajax({
          type:"GET",
          url: $('#c').attr('data-href'),
          data:{'c':c},
          success: function(response){
            console.log(response)
          },
          error: function(response){
            alert("error c")
          }
        })
  })
});
