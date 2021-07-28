$(document).ready(function () {
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
                url: $('.combo0').attr('data-href'),
                success: function(response){
                  for (var i in response.productdata){
                    $('#prod'+counter).append('<option value="'+response.productdata[i].product_name+'">'+response.productdata[i].product_name+'</option>')
                  }
                },
                error: function(response){
                  console.log("error not data found")
                }
              })
            var newRow= $(document.createElement('tr'))
            .attr("id", 'row' + counter)
            .attr("itemid", counter)
            newRow.html('<td><a id="del'+counter+'" href="#"> <i class="fa fa-trash" style="color: red;"aria-hidden="true"></i> </a></td><td><select name="prod'+counter+'" id="prod'+counter+'" placeholder="Select Product" class="editable-select form-control" ><option selected>-----------------Select Product-----------------</option></select></td><td><input type="text" class="tot form-control" id="unit'+ counter +'" name="unit'+ counter +'" readonly ></td><td><input type="number" min="0" step="any" class="form-control" id="rate'+counter+'" name="rate'+counter+'"></td><td><input type="number" min="0" class="addbtntext'+counter+' form-control" id="qty'+counter+'" name="qty'+counter+'"></td><td><input type="number" min="0" step="any" class="form-control" id="dis'+counter+'" name="dis'+counter+'"></td><td><input type="number" class="form-control" id="nr'+counter+'" name="nr'+counter+'"readonly  ></td><td><input type="text" class="tot form-control" id="tot'+counter+'" name="tot'+counter+'" readonly ></td>')
            newRow.appendTo('#itemtable')
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
            $('#rate'+counter).val(response)
          },
          error: function(response){
            console.log("error data not found")
          }
        })
        
        $.ajax({
          type:"GET",
          url: $('.punit').attr('data-href'),
          data:{'pname':pname},
          success: function(response){
            $('#unit'+counter).val(response)
          },
          error: function(response){
            console.log("error not data found")
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
  
  $('.addpurchase').hover(function (){
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
