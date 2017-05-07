function drawAIChart(msg) {
	var data = google.visualization.arrayToDataTable(msg);
	var options = {
			  title : 'ADROIT - Individual Performance Report',titleTextStyle: {bold: false},
			  
			  tooltip: {textStyle: {bold: true}},
			  isStacked: 'false' ,
			  width: 700,
			  height: 400,
			  pointSize: 4,
			  'is3D':true,
			  
			  vAxes: {0: {title: "Number of Masters Processed",titleTextStyle: {italic: false}} },
			  hAxis: {title: "Date",titleTextStyle: {italic: false} , slantedText: false},

			  //series: {0: {type: "line", targetAxisIndex: 0},1: {type: "bars"},3: {type: "bars"}}
	};
	var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
	chart.draw(data, options);
}



function individualProcess()
{

	fromDateFilter = document.getElementById('fromDateFilter').value;
	
	toDateFilter = document.getElementById('toDateFilter').value;
	usersList = document.getElementById('usersList').value;
	stationOfAi= document.getElementById('stationOfAi').value;
	
	values = 'fromDateFilter='+fromDateFilter+'&toDateFilter='+toDateFilter+'&usersList='+usersList+'&stationOfAi='+stationOfAi;
    $.ajax({
        url: "/process_it/extAiReport/",
        type: "POST",
        data: values,
        success: function(msg1){

        	    $("#fdate0").html("<td id='fdate0' >"+msg1['fromDateFilter']+"  to  "+msg1['toDateFilter']+" </td>")                        
        	    $("#fdate3").html("<td id='fdate3' >"+msg1['noOfAI']+" </td>") 
        	    $("#fdate4").html("<td id='fdate4' >"+msg1['cobEdRec']+" </td>")
        	    
        	    $("#fdate1").html("<td id='fdate1' >"+msg1['usersList']+" </td>")
        	    $("#fdate2").html("<td id='fdate2' >"+msg1['stationOfAi']+" </td>") 
        	    $("#fdate5").html("<td id='fdate5' >"+msg1['totalCobEd']+" </td>")
        	    $("#fdate6").html("<p>"+msg1['totalAi']+" </p>")
        	    

        	    
        	    $('#reptable').fadeIn('slow');
        	    var msg =new Array();
        	    var msgx =new Array(); 
        	    msg[0]="Date"
           	    msg[1]="AI Created"
           	    msg[2]="Total CODed"
           	    	
           	    msgx[0]=[msg1['fromDateFilter']]
           	    msgx[1]=[msg1['noOfAI']]
           	    msgx[2]=[msg1['totalCobEd']]
           	    	
        	    msg=[['Date','Total AI Created','Number of AI Created','Total CODed','Number of COB in Recovery'],[msg1['fromDateFilter']+" to "+msg1['toDateFilter'],msg1['totalAi'],msg1['noOfAI'],msg1['totalCobEd'],msg1['cobEdRec']  ]]

        	    drawAIChart(msg);
        	    
              //  $.unblockUI();
        	},
        beforeSend: function() {                
              //  $.blockUI({ message: '<br ><h1><img src="/static/img/ajax-loader2.gif" width="120" /></h1><br>' });
        	}   
    	});	
    
}

/*
function drawChart(msg) {
	//alert(msg);
	//var data = google.visualization.arrayToDataTable([['Date','Processed','Pending'],["07-09-13",0,1]]);
	var data = google.visualization.arrayToDataTable(msg);
	var options = {
		title : 'Performance',
		hAxis : {
			title : 'Date',
			titleTextStyle : {
				color : 'red'
			}
		}
	};
	var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
	chart.draw(data, options);
}
*/


function drawChart(msg) {
	var data = google.visualization.arrayToDataTable(msg);
	var options = {
			  title : 'ADROIT - Processed and Pending Report',titleTextStyle: {bold: false},
			  
			  tooltip: {textStyle: {bold: true}},
			  width: 800,
			  height: 400,
			  pointSize: 4,
			  legend : 'top', 
			  vAxes: {0: {title: "Masters",titleTextStyle: {italic: false}} },
			  hAxis: {title: "Date",titleTextStyle: {italic: false} , slantedText: true},

			  //series: {0: {type: "line", targetAxisIndex: 0},1: {type: "bars"},2: {type: "bars"}}
	};
	var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
	chart.draw(data, options);
}






function charts()
{   
    mawb = $("#selected_mawb").val();
    etaDate_list="";
    process_status="";
    
    Processed=0;
    Not_Processed=0;
    
    if(mawb.slice(-1)== ",")
    {
    	mawb = mawb.substring(0, mawb.length - 1);
    } 
    if(mawb == "")
    {
            alert("No Master selected!");
            return;
    }       
    mawb_arr = mawb.split(",");
      
    for(i = 0; i < mawb_arr.length; ++i) 
    {         
    	process = $("#"+mawb_arr[i]+"_row").children()[22].textContent;
        etaDate = $("#"+mawb_arr[i]+"_row").children()[8].textContent;
        etaDate_list += etaDate+","; 
        process_status += process+",";
        
/*        if (process_status == "Processed")
        	{
        	Processed++;
        	}
        else
        	{
        	Not_Processed++;
        	}
        	*/
    }

	count = document.getElementById('selected_mawb').value;
	count = count.split(',').length;
	
	json=[etaDate_list,Processed,Not_Processed];
	
	

	 
//		values = 'count='+count+"&etaDate_list="+etaDate_list+"&Processed="+Processed+"&Not_Processed="+Not_Processed;
	values = 'count='+count+"&mawb="+mawb+"&etaDate_list="+etaDate_list+"&process_status="+process_status;
//		alert(values);
//		return;
		
	    $.ajax({
	        url: "/process_it/charts/",
	        type: "POST",
	        data: values,
	        //contentType: "application/json",
	        //dataType : 'json',
	        success: function(msg){
	        	//alert(msg);
	        	//data = JSON.parse(msg);
	        	//alert(data);
	        	//alert(msg);
	        		//jsonObj = eval(msg);
	        		
	        		//alert(jsonObj);
	        		//$('#json_test').text(msg);
	        	//alert(msg);
	        		//drawChart([['Date', 'Processed', 'Pending'], ['07-10-13', '0', '1'],['07-10-13', '0', '1']]) ;
	        		drawChart(msg);
//	        		window.open ('/process_it/charts/', 'xxx', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=no, copyhistory=no, width=1000, height=500, top=60, left=100');
	        	},
	    	});		
		 
}












function logMawbSearch(type)
{   
	if( type=="search")
	{
		searchMawbNum = document.getElementById('searchMawbNum').value;
	    mawb_regex = /^(\d\d\d-\d\d\d\d\d\d\d\d|\d\d\d-\d\d\d\d\d\d\d\d([A-L]))$/;
	    
	    if(searchMawbNum.search(mawb_regex) == -1)
	    {               
	            alert('Master # should consist of ddd-ddddddddC format. Here all "d" are digits & "C" is any capital character between A-L or nothing, eg. 123-23342312A or 123-12345678!!');
	            $('#processingStatus').html("<img src='/static/img/error.gif' />");
	            return false;
	    }
		values = 'mawb='+searchMawbNum;
	    $.ajax({
	        url: "/process_it/displayLog/",
	        type: "POST",
	        data: values,
	        success: function(msg){
	        		$('#server_response').html(msg);
	                $.unblockUI();
	        	},
	        beforeSend: function() {                
	                $.blockUI({ message: '<br ><h1><img src="/static/img/ajax-loader2.gif" width="120" /></h1><br>' });
	        	}   
	    	});
	}
	
	else if( type=="all")
	{
	    $.ajax({
	        url: "/process_it/displayAllLog/",
	        success: function(msg){
	        		$('#server_response').html(msg);
	                $.unblockUI();
	        },
	        beforeSend: function() {                
	                $.blockUI({ message: '<br ><h1><img src="/static/img/ajax-loader2.gif" width="120" /></h1><br>' });
	        }   
	    });
	}

	else if( type=="mawbdate")
	{
		mawListDwDate = document.getElementById('mawListDwDate').value;
		mawListDwStation = document.getElementById('mawListDwStation').value;
		
		
		
		values = 'dateRet='+mawListDwDate+'&mawListDwStation='+mawListDwStation;
//		alert(values);
//		return;
		
	    $.ajax({
	        url: "/process_it/mawbByDate/",
	        type: "post",
	        data: values,
	        success: function(){
	        		//$('#server_response').html(msg);
	                $.unblockUI();
	                window.open('/process_it/mawbByDate/','');
	        },
	        beforeSend: function() {                
	                $.blockUI({ message: '<br ><h1><img src="/static/img/ajax-loader2.gif" width="120" /></h1><br>' });
	        }   
	    });
	}
}  



function growlErrorMsg(msg){

$.blockUI.defaults = { 
        growlCSS: { 
           width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                             
                  },
              },
$.growlUI('<h1 style="width:450px;top:100px;left:;right:px;color:red; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+ msg +'</h1>');  
}


function growlDoneMsg(msg){

$.blockUI.defaults = { 
        growlCSS: { 
           width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                       
                  },
              },
$.growlUI('<h1 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+ msg +'</h1>');  
}




function showtab(which){
document.getElementById(''+which+'').style.display='block';
}
function hidetab(which){
document.getElementById(''+which+'').style.display='none';
}

function datepicker() {
    $( "#datepicker" ).datepicker();
  }




function displayResult()
{
var table=document.getElementById("myTable");
var row=table.insertRow(2);
var cell1=row.insertCell(0);
var cell2=row.insertCell(1);
var cell3=row.insertCell(2);
var cell4=row.insertCell(3);
var cell5=row.insertCell(4);
var cell6=row.insertCell(5);
var cell7=row.insertCell(6);
var cell8=row.insertCell(7);
var cell9=row.insertCell(8);
var cell10=row.insertCell(9);
var cell11=row.insertCell(10);
var cell12=row.insertCell(11);
var cell13=row.insertCell(12);
var cell14=row.insertCell(13);
var cell15=row.insertCell(14);
var cell16=row.insertCell(15);
var cell17=row.insertCell(16);
var cell18=row.insertCell(17);
var cell19=row.insertCell(18);
var cell20=row.insertCell(19);
var cell21=row.insertCell(20);
var cell22=row.insertCell(21);
 
cell1.innerHTML='<img id="addMawb" name="addMawb" src="/static/img/save.gif" width="15" height="" onclick="savee(this);" /><img id="ShowHide1" src="/static/img/dw_arrow.png" width="12" height="" onclick="displayResult()" style="margin-left: 13px; opacity:0.5 " /> 	';	
cell2.innerHTML="<input type='text' onkeyup='ChangeCase(this);' id='station' name='station' autofocus='autofocus' >";
cell3.innerHTML='<input type="text" id="mawbNum" name="mawbNum" autofocus="autofocus" >';
cell4.innerHTML='<input type="text" id="consoleNumber" name="consoleNumber" autofocus="autofocus" >';
cell5.innerHTML='<input type="text" id="customer" name="customer" autofocus="autofocus" >';
cell6.innerHTML='<input type="text" onkeyup="ChangeCase(this);"  id="itInfo" name="itInfo" autofocus="autofocus" >';
cell7.innerHTML='<input type="text"  onkeyup="ChangeCase(this);"  id="flightCode" name="flightCode" autofocus="autofocus" >';
cell8.innerHTML='<input type="text" id="flightNum" name="flightNum" autofocus="autofocus" >';
cell9.innerHTML='<input type="text" id="etaDate" name="etaDate" placeholder="mm-dd-yy" autofocus="autofocus" onclick="datepicker()">';
cell10.innerHTML='<input type="text" id="etaTime" name="etaTime" autofocus="autofocus" >';
cell11.innerHTML='<input type="text" onkeyup="ChangeCase(this);"  id="shipmentStatus" name="shipmentStatus" autofocus="autofocus" >';
cell12.innerHTML='<input type="text" onkeyup="ChangeCase(this);"  id="source" name="source" autofocus="autofocus" >';
cell13.innerHTML='<input type="text" onkeyup="ChangeCase(this);"   id="speakWith" name="speakWith" autofocus="autofocus" >';
cell14.innerHTML='<input type="text" id="pmcOrLoose" name="pmcOrLoose" autofocus="autofocus" >';
cell15.innerHTML='<input type="text" id="slac" name="slac" autofocus="autofocus" >';
cell16.innerHTML='<input type="text" id="chgWeight" name="chgWeight" autofocus="autofocus" >';
cell17.innerHTML='<input type="text" onkeyup="ChangeCase(this);"   id="remarksInClass" name="remarksInClass" autofocus="autofocus" >';
cell18.innerHTML='<input type="text" id="oneFStatus" name="oneFStatus" autofocus="autofocus" >';
cell19.innerHTML='<input type="text" id="lastUpdatedDate" name="lastUpdatedDate" autofocus="autofocus" >';
cell20.innerHTML='<input type="text" id="lastUpdatedTime" name="lastUpdatedTime" autofocus="autofocus" >';
cell21.innerHTML='<input type="text" id="lastUpdatedByUser" name="lastUpdatedByUser" autofocus="autofocus" >';
cell22.innerHTML='<input type="text" id="oneFStatusComment" name="oneFStatusComment" autofocus="autofocus" >';

}
function savee(thisPointer)
{
	//alert(thisPointer.parent);
	objTr = thisPointer.parentElement.parentElement;
	//alert(objTd);
    //objTr = objTd.parent();
    var station = objTr.children[1].childNodes[0].value;
    var mawbNum = objTr.children[2].childNodes[0].value;    
    var consoleNumber = objTr.children[3].childNodes[0].value;
    var customer = objTr.children[4].childNodes[0].value;
    var itInfo = objTr.children[5].childNodes[0].value;
    var flightCode = objTr.children[6].childNodes[0].value;
    var flightNum = objTr.children[7].childNodes[0].value;
    var etaDate = objTr.children[8].childNodes[0].value;
    var etaTime = objTr.children[9].childNodes[0].value;
    var shipmentStatus = objTr.children[10].childNodes[0].value;
    var trackSource = objTr.children[11].childNodes[0].value;
    var speakWith = objTr.children[12].childNodes[0].value;
    var pmcOrLoose = objTr.children[13].childNodes[0].value;
    var slac = objTr.children[14].childNodes[0].value;
    var chgWeight = objTr.children[15].childNodes[0].value;;
    var remarksInClass = objTr.children[16].childNodes[0].value;
    var oneFStatus = objTr.children[17].childNodes[0].value;
    var lastUpdatedDate = objTr.children[18].childNodes[0].value;
    var lastUpdatedTime = objTr.children[19].childNodes[0].value;;
    var lastUpdatedByUser = objTr.children[20].childNodes[0].value;
    var oneFStatusComment = objTr.children[21].childNodes[0].value;
   
    mawb_regex = /^(\d\d\d-\d\d\d\d\d\d\d\d|\d\d\d-\d\d\d\d\d\d\d\d([A-L]))$/;

    
    if(mawbNum.search(mawb_regex) == -1)
    {               
            alert('Master # should consist of ddd-ddddddddC format. Here all "d" are digits & "C" is any capital character between A-L or nothing, eg. 123-23342312A or 123-12345678!!');
            $('#processingStatus').html("<img src='/static/img/error.gif' />");
            return false;
    }
    
    date_regex= /^[0-9]{2}\-[0-9]{2}\-[0-9]{2}$/;
    
//    if(etaDate=='')
    
    if(etaDate.search(date_regex) == -1)
    {
            alert('ETA Date is a mandatory field & should be of format MM-DD-YY !');
            $('#processingStatus').html("<img src='/static/img/error.gif' />");
            return false;
    } 
 
    
//  alert(oneFStatusComment);
//  return;      
    
    
            values = 'station='+station+'&mawbNum='+mawbNum+'&consoleNumber='+consoleNumber+'&customer='+customer+'&itInfo='+itInfo+'&flightCode='+flightCode+'&flightNum='+flightNum+'&etaDate='+etaDate+'&etaTime='+etaTime+'&shipmentStatus='+shipmentStatus+'&trackSource='+trackSource+'&speakWith='+speakWith+'&pmcOrLoose='+pmcOrLoose+'&slac='+slac+'&chgWeight='+chgWeight+'&remarksInClass='+remarksInClass+'&oneFStatus='+oneFStatus+'&lastUpdatedDate='+lastUpdatedDate+'&lastUpdatedTime='+lastUpdatedTime+'&lastUpdatedByUser='+lastUpdatedByUser+'&oneFStatusComment='+oneFStatusComment;
//            values = 'station='+station+'&mawbNum='+mawbNum+'&consoleNumber='+consoleNumber+'&customer='+customer+'&flightCode='+flightCode+'&flightNum='+flightNum+'&etaDate='+etaDate+'&etaTime='+etaTime+'&shipmentStatus='+shipmentStatus+'&trackSource='+trackSource+'&speakWith='+speakWith+'&pmcOrLoose='+pmcOrLoose+'&slac='+slac+'&chgWeight='+chgWeight+'&remarksInClass='+remarksInClass+'&oneFStatus='+oneFStatus+'&lastUpdatedDate='+lastUpdatedDate+'&lastUpdatedTime='+lastUpdatedTime+'&lastUpdatedByUser='+lastUpdatedByUser+'&oneFStatusComment='+oneFStatusComment;


           
     
            $.ajax({
                url: "/process_it/validateMawbEntry/",
                type: "post",
                data: values,
                success: function(msg){
//                	$("#addMawb").attr("src","/static/img/save.gif");
                        if((msg['exists'])==1)
                                {
                        	msg= 'MAWB Exist in Database...!';
                            return growlErrorMsg(msg);
                                }
                        
                        else if(msg['exists']==2)
                        {
                        	msg= ' MAWB Deleted from here but Exist in the DB...';
                            return growlErrorMsg(msg);
                        }                        
                        
                        else
                                {
                                                                                               	   
                               $.ajax({
                                   url: "/process_it/addMawbEntry/",
                                   type: "post",
                                   data: values,
                                   success: function(msg){
                         //            $('#addid').html("<img src='/static/img/done.gif' />");                 /////////// DONE     
                                       $("#addMawb").attr("src","/static/img/save.gif");    
                                	   msg= 'Saving Completed..';
                                       return growlDoneMsg(msg);   
                                   },
                                   beforeSend: function() {                                                                                /////////// PROCESSING
                              //           $("#addid").html("<img src='/static/img/processing.gif' />");  
//                                	   $("#addMawb").attr("src","/static/img/processing.gif");
                                	   
                                	   msg= 'Please Wait..';
                                       return growlDoneMsg(msg);
                                                                                                                                                      
                                   },
                                   error:function(){                                                                                                               /////////// ERROR
                                           $('#addid').html("<img src='/static/img/error.gif' />");
                                   }   
                               });                                         	
                            }
                	},
            beforeSend: function() {                                                                                /////////// PROCESSING
                  	   $("#addMawb").attr("src","/static/img/processing.gif");
                  	                                                                                                                                           
                     }
            
            
            
            
            
            });       
}




/*

function saveNewlyAddedMAwb(newObjTr)
{
        //alert('hiii'+newObjTr.children()[2].innerHTML);
        //ar first_parent_tr = $('#'+id+'_update').parent().parent();
        
        //var mawb_id = $('#'+id+'_mawb_id').val();
//var actionType = $('#'+id+'_actionType').val();
        var station = newObjTr.children()[1].innerHTML;
        var mawbNum = newObjTr.children()[2].innerHTML; 
        var consoleNumber = newObjTr.children()[3].innerHTML;
        var customer = newObjTr.children()[4].innerHTML;
        var itInfo = newObjTr.children()[5].innerHTML;
        var flightCode = newObjTr.children()[6].innerHTML;
        var flightNum = newObjTr.children()[7].innerHTML;
        var etaDate = newObjTr.children()[8].innerHTML;
        var etaTime = newObjTr.children()[9].innerHTML;
        var shipmentStatus = newObjTr.children()[10].innerHTML;
        var trackSource = newObjTr.children()[11].innerHTML;
        var speakWith = newObjTr.children()[12].innerHTML;
        var pmcOrLoose = newObjTr.children()[13].innerHTML;
        var slac = newObjTr.children()[14].innerHTML;   
        var chgWeight = newObjTr.children()[15].innerHTML;
        var remarksInClass = newObjTr.children()[16].innerHTML; 
        var oneFStatus = newObjTr.children()[17].innerHTML;
        var lastUpdatedDate = newObjTr.children()[18].innerHTML;
        var lastUpdatedTime = newObjTr.children()[19].innerHTML;
        var lastUpdatedByUser = newObjTr.children()[20].innerHTML;
        var oneFStatusComment = newObjTr.children()[21].innerHTML;
        
        
        
        
        mawb_regex = /^(\d\d\d-\d\d\d\d\d\d\d\d|\d\d\d-\d\d\d\d\d\d\d\d([A-L]))$/;
        
        if(mawbNum.search(mawb_regex) == -1)
        {               
                alert('Master # should consist of ddd-ddddddddC format. Here all "d" are digits & "C" is any capital character between A-L or nothing, eg. 123-23342312A or 123-12345678!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        else
        {               
//              alert(mawbNum);
//              return;
                $.ajax({
                url: "/process_it/chkHasMawb/",
                type: "post",
                data: "id="+mawbNum+"&chkmawb="+mawbNum,
                
                success: function(resp_list){                   
                                $.each(resp_list, function(key,val){
                                        if(val == 1){
        //                                      $('#load_resp').html("<img src='/static/img/done.gif' title='Mawb does not exist in database!, hence added but without station' />");                                           
                                                //alert("Mawb exist in database!");
                                        //      return;
                                                $.blockUI.defaults = { 
                                                        growlCSS: { 
                                                                width:    '450px', 
                                                                top:      '100px', 
                                                                left:     '', 
                                                                right:    '20px', 
                                                                border:   'none', 
                                                                padding:  '5px', 
                                                                opacity:   0.8, 
                                                                cursor:    null, 
                                                                color:    '#fff', 
                                                                backgroundColor: '#000',                                                             
                                                            },
                                                        },
                                        $.growlUI('<h1 style="width:450px;top:100px;left:;right:px;color:red; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">MAWB Exist in Database...</h1>');  
                                      

                                        }
                                        
                                        else if(val == 0){
                                                $('#load_resp').html("<img src='/static/img/error.gif' title='Mawb exist in database!' />");  
        //                                      alert("Mawb does not exist in database!, hence added but without station");                                             
        
                                                values = 'station='+station+'&mawbNum='+mawbNum+'&consoleNumber='+consoleNumber+'&customer='+customer+'&itInfo='+itInfo+'&flightCode='+flightCode+'&flightNum='+flightNum+'&etaDate='+etaDate+'&etaTime='+etaTime+'&shipmentStatus='+shipmentStatus+'&trackSource='+trackSource+'&speakWith='+speakWith+'&pmcOrLoose='+pmcOrLoose+'&slac='+slac+'&chgWeight='+chgWeight+'&remarksInClass='+remarksInClass+'&oneFStatus='+oneFStatus+'&lastUpdatedDate='+lastUpdatedDate+'&lastUpdatedTime='+lastUpdatedTime+'&lastUpdatedByUser='+lastUpdatedByUser+'&oneFStatusComment='+oneFStatusComment;
                                                $.ajax({
                                                url: "/process_it/addMawbEntry/",
                                                type: "post",
                                                data: values,
                                                success: function(msg){
                                          //            $('#addid').html("<img src='/static/img/done.gif' />");                 /////////// DONE      
                                                $.blockUI.defaults = { 
                                                                growlCSS: { 
                                                                        width:    '450px', 
                                                                        top:      '100px', 
                                                                        left:     '', 
                                                                        right:    '20px', 
                                                                        border:   'none', 
                                                                        padding:  '5px', 
                                                                        opacity:   0.8, 
                                                                        cursor:    null, 
                                                                        color:    '#fff', 
                                                                        backgroundColor: '#000',                                                             
                                                                    },
                                                                },
                                                $.growlUI('<h1 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">Saving Completed..</h1>');  
                                                //<img src="/static/img/light.jpg" alt="searce logo" align="left" width="150px"/>       
                                                },
                                                beforeSend: function() {                                                                                /////////// PROCESSING
                                           //           $("#addid").html("<img src='/static/img/processing.gif' />");  
                                                        $.blockUI.defaults = { 
                                                                        growlCSS: { 
                                                                                width:    '450px', 
                                                                                top:      '100px', 
                                                                                left:     '', 
                                                                                right:    '20px', 
                                                                                border:   'none', 
                                                                                padding:  '5px', 
                                                                                opacity:   0.8, 
                                                                                cursor:    null, 
                                                                                color:    '#fff', 
                                                                                backgroundColor: '#000', 
                                                                                '-webkit-border-radius': '20px', 
                                                                                '-moz-border-radius':    '20px' 
                                                                            },
                                                                        },
                                                               $.growlUI('<h1 style="width:450px;top:100px;left:;right:20px;color:#FF6666; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; "  >Please Wait.. </h1>');                                                                                                                  
                                                },
                                                error:function(){                                                                                                               /////////// ERROR
                                                        $('#addid').html("<img src='/static/img/error.gif' />");
                                                }   
                                            });                                                 
                                        
                                        }
                        });
                },
                beforeSend: function() {                
                        $('#load_resp').html("<img src='/static/img/processing.gif' />");
                }
            });
        }

}





function addMawbRow(thisPointer)
{
        //alert('hi');
        //alert(thisPointer.id);
        objTd = $('#'+thisPointer.id).parent();
        objTr = objTd.parent();
        newObjTr = objTr.clone(true); 
        objTbody = objTr.parent();
        //alert(objTbody.childNodes[objTr.index()]);
        newObjTr.id= objTbody.id+Math.floor((Math.random()*100)+1); ;
        newObjTr.css('background-color','#DBEAF9');


        firstTd = newObjTr.children()[0];
        firstTd.innerHTML="<img class='styleCursorType' title='Click here to save!' src='/static/img/save.gif' onclick=saveNewlyAddedMAwb(newObjTr); style='padding:10px' /><h3 id='addid'></h3>";
        
        for(i=1; i<newObjTr.children().length; i++)
        {
                 newObjTr.children()[i].innerHTML='';
                 newObjTr.children()[i].id='';
        }
        
        newObjTr.insertAfter(objTr);
        //alert($('#'+thisPointer.id).innerH);
        
}



*/
 
 


function mawbInsert()
{       
        mawbNum = document.getElementById('mawbNum').value;
        
       
        
        mawb_regex = /^(\d\d\d-\d\d\d\d\d\d\d\d|\d\d\d-\d\d\d\d\d\d\d\d([A-L]))$/;
 
        if(mawbNum.search(mawb_regex) == -1)
        {               
                alert('Master # should consist of ddd-ddddddddC format. Here all "d" are digits & "C" is any capital character between A-L or nothing, eg. 123-23342312A or 123-12345678!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
      
        else
                {
               
                values = 'mawbNum='+document.getElementById('mawbNum').value;
//              values = mawbNum;
//              alert("Done ! "+values);
                $.ajax({
                        url: "/process_it/insertMawb/",
                        type: "post",
                        data: values,         
                        success: function(resp_list){
                                $.each(resp_list, function(key,val)
                                                {
                                        if(val == 1){
                                                $('#load_resp').html("<br><br><img src='/static/img/done.gif' title='Mawb exist in database!' />");                                             
                                                alert("                     Done..! \nNew Mawb added but without station.");
                                                }
                                        else if(val == 0){
                                                $('#load_resp').html("<img src='/static/img/error.gif' title='Mawb does not exist in database!, hence added but without station' />");
                                                alert("Warning: Mawb Number exist in database ! ");
                                                }
                                
                                                });
                
            },
            beforeSend: function() {            
 
            }
         });
                }
}









$(document).ready(function() {
$("#HiddenRowsNotice").html("<tr><td colspan='2'> <a href='#'>>> some rows hidden <<</a></td></tr>");
$("#ShowHide").html("");
$("#HiddenRows, #HiddenRows1").hide();

$("#ShowHide1").html("");
$("#HiddenRows1").hide();

$('#ShowHide,#HiddenRowsNotice').click( function() {
$('#HiddenRows').toggle();      
$('#HiddenRowsNotice').toggle();
});
});
$('#something').click( function() {
    $('.Table_Middle').hide();
    $('.Show_Rows').show();
});
$('.Show_Rows').click( function() { 
    $('.Show_Rows').hide();
    $('.Table_Middle').show();
});






function datasourceCount(fromDateFilter,toDateFilter)
{
 
        if ( fromDateFilter == '' || toDateFilter == '')
        {
                alert('Please enter date!');
                return;
        }
        
        values = 'fromDateFilter='+fromDateFilter+'&toDateFilter='+toDateFilter;
        $.ajax({
        url: "/process_it/getDashboardCounts/",
        type: "post",
        data: values,
        success: function(msg){

                $("#lax_cob").html(msg['lax_cob']);
                $("#lax_bo").html(msg['lax_bo']);
                $("#sfo_cob").html(msg['sfo_cob']);
                $("#sfo_bo").html(msg['sfo_bo']);
                
                $("#dfw_cob").html(msg['dfw_cob']);
                $("#dfw_bo").html(msg['dfw_bo']);
                $("#iah_cob").html(msg['iah_cob']);
                $("#iah_bo").html(msg['iah_bo']);       
                
                $("#mail_uniden_count").html(msg['mail_uniden_count']);
                $("#mail_oos_count").html(msg['mail_oos_count']);
                $("#mail_lax_count").html(msg['mail_lax_count']);
                $("#mail_sfo_count").html(msg['mail_sfo_count']);


                $("#processingStatus").html("");
                
                $.unblockUI();
        },
        beforeSend: function() {                
   //           $("#processingStatus").html('<h1><img src="/static/img/ajax-loader.gif" /> Just a moment...</h1>');
                $.blockUI({ message: '<br ><h1><img src="/static/img/ajax-loader2.gif" width="120" /></h1><br>' });
        
        }
     });
               
}


        

function laxDetailBody()
{
        
        $('#airLineTable').handsontable({         
                  colHeaders: ["prefix#","prefix","Airline Name", "Ph#", "Ext#", "Fax#", "FIRMs", "Other#", "Business Hrs", "Handling Agent"],
                  data:data_lax,
                  
                  columns: [
                    
                    {data: 'prefixNum', type: {renderer: descriptionRenderer}},
                    {data: 'prefix', type: {renderer: descriptionRenderer}},
                    {data: 'airlineName', type: {renderer: descriptionRenderer}},
                    {data: 'phoneNum', type: {renderer: descriptionRenderer}},
                    {data: 'extNum', type: {renderer: descriptionRenderer}},
                    {data: 'faxNum', type: {renderer: descriptionRenderer}},
                    {data: 'firms', type: {renderer: descriptionRenderer}},
                    {data: 'otherNum', type: {renderer: descriptionRenderer}},
                    {data: 'businessHrs', type: {renderer: descriptionRenderer}},
                    {data: 'handlingAgent', type: {renderer: descriptionRenderer}}
                  ],
                  
                });
        
        //$('#openMenuImage').append("<img src='/static/img/rightOut.png'>");
}



function highLightTR()
{
        
        $('.htCore tbody tr').each( function() {
                
                if(this.children[0].children[6].value == 'True')
                        {
                                $(this).addClass("styleRowBG");
                        }
                
                $(this).attr("id",this.children[2].textContent+"_row");
                $($("#"+this.children[2].textContent+"_row td")[16]).attr("title",this.children[0].children[7].value);
        } );
                                                              //          gets called in prealertProcessing.html <body ()>
}                               

function new_addMawbFun(id,type)
{
        var first_parent_tr = $('#'+id+'_update').parent().parent();
        
        var mawb_id = $('#'+id+'_mawb_id').val();
        var actionType = $('#'+id+'_actionType').val();
        
        var station = first_parent_tr.children()[1].innerHTML;
        var mawbNum = first_parent_tr.children()[2].innerHTML;  
        var consoleNumber = first_parent_tr.children()[3].innerHTML;
        var customer = first_parent_tr.children()[4].innerHTML;
        var itInfo = first_parent_tr.children()[5].innerHTML;
        var flightCode = first_parent_tr.children()[6].innerHTML;
        var flightNum = first_parent_tr.children()[7].innerHTML;
        var etaDate = first_parent_tr.children()[8].innerHTML;
        var etaTime = first_parent_tr.children()[9].innerHTML;
        var shipmentStatus = first_parent_tr.children()[10].innerHTML;
        var trackSource = first_parent_tr.children()[11].innerHTML;
        var speakWith = first_parent_tr.children()[12].innerHTML;
        var pmcOrLoose = first_parent_tr.children()[13].innerHTML;
        var slac = first_parent_tr.children()[14].innerHTML;    
        var chgWeight = first_parent_tr.children()[15].innerHTML;
        var remarksInClass = first_parent_tr.children()[16].innerHTML;  
        var oneFStatus = first_parent_tr.children()[17].innerHTML;
        var lastUpdatedDate = first_parent_tr.children()[18].innerHTML;
        var lastUpdatedTime = first_parent_tr.children()[19].innerHTML;
        var lastUpdatedByUser = first_parent_tr.children()[20].innerHTML;
        var oneFStatusComment = first_parent_tr.children()[21].innerHTML;
        
        
        date_regex = /^(0[1-9]|1[012])[- . \/](0[1-9]|[12][0-9]|3[01])[- .\/]\d\d$/;
        time_regex = /^(0[0-9][0-5][0-9]|1[0-9][0-5][0-9]|2[0-3][0-5][0-9])$/;
        mawb_regex = /^(\d\d\d-\d\d\d\d\d\d\d\d|\d\d\d-\d\d\d\d\d\d\d\d([A-L]))$/;
        hawb_regex = /^([a-z]|[A-Z]|[0-9]|[-])*$/;
        pmc_regex = /^(Loose|\d\d|\d)$/;
        cust_regex = /^([a-z]|[A-Z]|[0-9]|[ ])*$/;
             
    
        if(trackSource == 'CALL')
        {
                if(speakWith=='')
                {
                        alert('S/W is a mandatory field!');
                        $('#processingStatus').html("<img src='/static/img/error.gif' />");
                        return false;
                }
        }
        
        //Mandatory fields
        if(mawbNum=='')
        {
                alert('Master # is a mandatory field!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        if(etaDate=='')
        {
                alert('ETA Date is a mandatory field!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        if(shipmentStatus=='')
        {
                alert('Shipment Status is a mandatory field!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        //Number fields
        if(isNaN(slac))
        {
                alert('SLAC(CTNs) should be a number!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        if(isNaN(consoleNumber))
        {
                alert('Consol # should be a number!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        if(isNaN(chgWeight))
        {
                alert('CHG. WGHT. should be a number!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        //Field specific rules
        if(mawbNum.search(mawb_regex) == -1)
        {               
                alert('Master # should consist of ddd-ddddddddC format. Here all "d" are digits & "C" is any capital character between A-L or nothing, eg. 123-23342312A or 123-12345678!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        if(consoleNumber != "" && consoleNumber.length != 6)
        {
                alert('Consol # must be 6 digits!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        if(flightCode != "" && flightCode.length > 20)
        {
                alert('Flight Code lenght must be minimum 2 Characters Maximum 19 Characters !!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }

        
        if(flightCode == "TRUCK" && flightNum != "")
        {
                alert('Flight Number should be empty !!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        if(slac != "" && slac.length > 5)
        {
                alert('SLAC(CTNs) must be upto 5 digits!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }       
        
        if(chgWeight != "" && chgWeight.length > 5)
        {
                alert('CHG. WGHT. must be upto 5 digits!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        if(customer != "" && customer.search(cust_regex) == -1)
        {
                alert('Customer must contain only alpha-numeric characters!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        if(etaTime.search(time_regex) == -1 && etaTime != "")
        {
                alert('ETA Time must have hhmm (0000-2359) format!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;   
                        
        }
        
	        if(etaDate.search(date_regex) == -1 && etaDate != "")
	        {
	                alert('ETA Date must have mm-dd-yy format!!');
	                $('#processingStatus').html("<img src='/static/img/error.gif' />");
	                return false;
	        }
        	
        	
        
        
        
        if(type=='update')
        {
                
                //ajaxWithSerialize('n','processingStatus','/process_it/mawbAction/',$('#formid_'+id).serialize()); //original update call
                
                values = 'mawb_id='+mawb_id+'&station='+station+'&mawbNum='+mawbNum+'&consoleNumber='+consoleNumber+'&customer='+customer+'&flightCode='+flightCode+'&flightNum='+flightNum+'&etaDate='+etaDate+'&etaTime='+etaTime+'&itInfo='+itInfo+'&shipmentStatus='+shipmentStatus+'&trackSource='+trackSource+'&speakWith='+speakWith+'&pmcOrLoose='+pmcOrLoose+'&slac='+slac+'&chgWeight='+chgWeight+'&remarksInClass='+remarksInClass+'&oneFStatus='+oneFStatus+'&lastUpdatedDate='+lastUpdatedDate+'&lastUpdatedTime='+lastUpdatedTime+'&lastUpdatedByUser='+lastUpdatedByUser+'&oneFStatusComment='+oneFStatusComment;
   
//                alert(values);
  //              return;
                
                //ajaxWithSerialize('n','processingStatus','/process_it/mawbAction/','actionType=delete&'+values);
                
                //Calling url
                    $.ajax({
                        url: "/process_it/updateMawbEntry/",
                        type: "post",
                        data: values,
                        success: function(msg){
                                $("#"+id+"_update").attr("src","/static/img/save.gif");
                                first_parent_tr.children()[18].innerHTML=msg['date'];
                                first_parent_tr.children()[19].innerHTML=msg['time'];
                                first_parent_tr.children()[20].innerHTML=msg['name'];
                                first_parent_tr.children('.mawbNum').css("background-color","#F7F2B2");
                                
                                
                                first_parent_tr.css("background-color","#F7F2B2");
                                if(msg['cob'])
                                                {
                                                        $('#'+id+'_row').css('display','None');
                                                }
                        },
                        beforeSend: function() {                
                                $("#"+id+"_update").attr("src","/static/img/processing.gif");
                                 
                        }
                    });
                
                
        }
        
        if(type=='add')
        {
                var values = $('#mawb_entry_form').serialize(); 
              
                    $.ajax({
                        url: "/process_it/addMawbEntry/",
                        type: "post",
                        data: values,
                        success: function(msg){
                                
                                location.reload();      
                                $('#processingStatus').html("<img src='/static/img/done.gif' />");
                        },
                        beforeSend: function() {                
                                $("#processingStatus").html("<img src='/static/img/processing.gif' />");
                                 
                        },
                        error:function(){
                                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                        }   
                    });
        }
                
}

function tempBody()
{
        
        $('#dataTable').handsontable({    
                  //colHeaders: ["<div id=openCloseMenu class='styleGreyBG styleButtonAlign'> <a class=rightMenuAction id=openMenuImage > </a></div>",
                   //            "Station", "Master#", "Consol#", "Customer", "IT Information", "Flight Code", "Flight#", "ETA Date", "ETA Time", "Shipment Status","Source","S/W","PMC/LOOSE","SLAC","CHG. WGHT.","Remarks in CLASS","1F Status","Last Updated Date","Last Updated Time","Updated By","Comment"],
                  data:data,
                  
                  columns: [
                    {data: 'isActive',type: {renderer: descriptionRenderer}},
                    {data: 'station',type: {renderer: stationRenderer}},
                    {data: 'mawbNum',type: {renderer: mawbNumRenderer}},
                    {data: 'consoleNumber',type: {renderer: consoleNumberRenderer}},
                    {data: 'customer',type: {renderer: customerRenderer}},
                    {data: 'itInfo',type: {renderer: itInfoRenderer}},
                    {data: 'flightCode',type: {renderer: flightCodeRenderer}},
                    {data: 'flightNum',type: {renderer: flightNumRenderer}},
                    {data: 'etaDate',type: {renderer: etaDateRenderer}},
                    {data: 'etaTime',type: {renderer: etaTimeRenderer}},
                    {data: 'shipmentStatus',type: {renderer: shipmentStatusRenderer}},
                    {data: 'trackSource',type: {renderer: trackSourceRenderer}},
                    {data: 'speakWith',type: {renderer: speakWithRenderer}},
                    {data: 'pmcOrLoose',type: {renderer: pmcOrLooseRenderer}},
                    {data: 'slac',type: {renderer: slacRenderer}},
                    {data: 'chgWeight',type: {renderer: chgWeightRenderer}},
                    {data: 'remarksInClass',type: {renderer: remarksInClassRenderer}},
                    {data: 'oneFStatus',type: {renderer: oneFStatusRenderer}},
                    {data: 'lastUpdatedDate',type: {renderer: lastUpdatedDateRenderer}},
                    {data: 'lastUpdatedTime',type: {renderer: lastUpdatedTimeRenderer}},
                    {data: 'lastUpdatedByUser',type: {renderer: lastUpdatedByUserRenderer}},
                    {data: 'oneFStatusComment',type: {renderer: oneFStatusCommentRenderer}},    
                    {data: 'spProStatus',type: {renderer: spProStatusRenderer}}                       
                    
                       
                  ]  
        
                });
        
        //$('#openMenuImage').append("<img src='/static/img/rightOut.png'>");		
}




function linkedin_call()
{
         $.ajax({
                url: "http://api.linkedin.com/v1/people/~/connections?format=json",
                type: "get",
                success: function(msg){
                        alert(msg['message']);
                }
            });
}

function validateRebookMawb()
{
        var values = $('#rebook_entry_form').serialize();       
        if($('#reebookdMawbNum').val() == "")
        {
                alert('please enter Master #!!');
                return false;
        }
        else
        {
                //Calling url
            $.ajax({
                url: "/process_it/rebookEntry/",
                type: "post",
                data: values,
                success: function(msg){
                        if(!msg['exists'])
                                {
                                alert('There is no master for rebooking or master is already visible.. Please create new one!!');
                                }
                }
            });
                
        }
        
}

function select_all()
{
        var chk_box;
        var child_trs = $("#dataTable tbody")[0].children;
        
        var mbl_list = [];
        
        if ($('#chkAll').is(':checked'))
        {
                $.each(child_trs, function(i) {
                    if(this.id.search('_row') != -1)
                    {                                   
                        chk_box = $('#'+this.id+' td')[0].children[0].id;
                        child_tds = $('#'+this.id+' td').children();
                                
                        if(!$('#'+child_tds[0].id).is(':checked'))                      
                        {
                                $.each(child_tds, function(i){
                                        
                                        if(this.id.search('mawbNum')!=-1)
                                                {
                                                        mbl_list.push(""+this.value);                                   
                                                }
                                        
                                });
                                //mbl_id = $('#'+this.id+' td')[4].children[0].id;
                                
                                $("#"+chk_box).attr('checked', true);
                        }
                    }   
                        
                });
                
                $("#selected_mawb").val(mbl_list);
        }
        else
        {
                $.each(child_trs, function(i) {
                    if(this.id.search('_row') != -1)
                    {
                        chk_box = $('#'+this.id+' td')[0].children[0].id;
                        child_tds = $('#'+this.id+' td').children();
                        if($('#'+child_tds[0].id).is(':checked'))                       
                        {
                                $.each(child_tds, function(i){
                                        
                                        if(this.id.search('mawbNum')!=-1)
                                                mbl_list.push(""+this.value);
                                });
                                //mbl_id = $('#'+this.id+' td')[4].children[0].id;
                                $("#"+chk_box).attr('checked', false);
                        }
                    }   
                        
                });
                
                $("#selected_mawb").val('');
                
        }
        //alert(mbl_list);
        
}

function select_all_new()
{
        var chk_box;
        var child_trs = $("#dataTable tbody")[0].children;
        
        var mbl_list = [];
        

                
        if ($('#chkAll').is(':checked'))
        {
                $.each(child_trs, function(i) {
                                                        
                        chk_box = this.children[0].children[2].id;
                        
                                mbl_list.push(""+chk_box.split('_')[0]);
                            
                        $("#"+chk_box).attr('checked', true);
                        
                });                     
                
                $("#selected_mawb").val(mbl_list);
        }
        else
        {
                $.each(child_trs, function(i) {
                    
                        chk_box = this.children[0].children[2].id;
                        
                        if($('#'+chk_box).is(':checked'))                               
                        {
                                 mbl_list.push(""+chk_box.split('_')[0]);
                                
                                $("#"+chk_box).attr('checked', false);
                        }
                        
                        
                });
                
                $("#selected_mawb").val('');
                
        }

        
        
}

function select_all_cob()
{
        var chk_box;
        var child_trs = $("#masterDataTable tbody")[0].children;
        
        var mbl_list = [];
        
        if ($('#chkAll').is(':checked'))
        {
                $.each(child_trs, function(i) {
                                                        
                        chk_box = this.children[0].children[0].id;
                        
                                mbl_list.push(""+chk_box.split('_')[0]);
                            
                        $("#"+chk_box).attr('checked', true);
                        
                });
                
                $("#selected_mawb").val(mbl_list);
        }
        else
        {
                $.each(child_trs, function(i) {
                    
                        chk_box = this.children[0].children[0].id;
                        
                        if($('#'+chk_box).is(':checked'))                               
                        {
                                 mbl_list.push(""+chk_box.split('_')[0]);
                                
                                $("#"+chk_box).attr('checked', false);
                        }
                });
                
                $("#selected_mawb").val('');
                
        }
        
        
}

function check_uncheck(mawb)
{       
        //alert(this);
        //alert($("#selected_mawb").val());
        
        if($("#"+mawb+"_chkbox").attr("checked"))
                $("#selected_mawb").val(mawb+","+$("#selected_mawb").val());
        else
                $("#selected_mawb").val($("#selected_mawb").val().replace(mawb+",",""));
}

function completeCOBToMasters()
{
        mawb = $("#selected_mawb").val();
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }
        mawb_arr = mawb.split(",");
        
        var answer = confirm("Please confirm the deletion of records!!");
        
        if (answer)
        {       
                for(i = 0; i < mawb_arr.length; ++i) 
                {
                        $('#'+mawb_arr[i]+'_row').css('display','None');                
                }       
                ajaxWithSerialize('n','processingStatus','/process_it/completeCOBToMasters/','mawb_arr='+mawb_arr);                     
        }
        else{
                return false;           
        }
        
}

function moveMastersToPAP()
{
        mawb = $("#selected_mawb").val();
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }
        mawb_arr = mawb.split(",");
        
        var answer = confirm("Please confirm the deletion of records!!");
        
        if (answer)
        {       
                for(i = 0; i < mawb_arr.length; ++i) 
                {
                        $('#'+mawb_arr[i]+'_row').css('display','None');                
                }       
                ajaxWithSerialize('n','processingStatus','/process_it/moveMastersToPAP/','mawb_arr='+mawb_arr);                 
        }
        else{
                return false;           
        }
      
}

function deleteMasters()
{
        mawb = $("#selected_mawb").val();
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }
        mawb_arr = mawb.split(",");     
        
        var answer = confirm("Please confirm the deletion of records!!");
        if (answer)
        {       
                for(i = 0; i < mawb_arr.length; ++i) 
                {
                        $('#'+mawb_arr[i]+'_row').css('display','None');                
                }       
                ajaxWithSerialize('n','processingStatus','/process_it/deleteMasters/','mawb_arr='+mawb_arr);                    
        }
        else{
                return false;           
        }
}

function send_masters(send_type)
{
        mawb = $("#selected_mawb").val();
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }
        mawb_arr = mawb.split(",");     
        
        if(send_type == 'delete')
                {var answer = confirm("Please confirm the deletion of records!!");}
        else if(send_type == 'complete')
                {var answer = confirm("Please confirm the COB completed for records!!");}
        else if(send_type == 'moveBack')
                {var answer = confirm("Please confirm the moving back to pap for records!!");}
        if (answer)
        {       
                for(i = 0; i < mawb_arr.length; ++i) 
                {
                        $('#'+mawb_arr[i]+'_row').css('display','None');                
                }       
                $("#selected_mawb").val('');
                if(send_type == 'delete')
                        {ajaxWithSerialize('n','processingStatus','/process_it/deleteMasters/','mawb_arr='+mawb_arr);}
                else if(send_type == 'complete')
                        {ajaxWithSerialize('n','processingStatus','/process_it/completeCOBToMasters/','mawb_arr='+mawb_arr);}
                else if(send_type == 'moveBack')
                        {ajaxWithSerialize('n','processingStatus','/process_it/moveMastersToPAP/','mawb_arr='+mawb_arr);}
                                        
        }
        else{
                return false;           
        }
}







function create_ai_file(mawb,username,password)
{
        //alert('hio');
        //return;
        username = $('#class_uname').val();
        password = $('#class_pass').val();
        mawb = $("#selected_mawb").val();
        station_list="";
        
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }       
        flag=0;
    invalid_mawbs ="";
    
    
    /*
        mawb_arr = mawb.split(",");   
        
        for(i = 0; i < mawb_arr.length; ++i) 
        {
                
                if(mawb_arr[i]=="")
                        continue;
                if($("#"+mawb_arr[i]+"_row").children()[3].textContent=='')
                {
                        invalid_mawbs += mawb_arr[i] + ",";
                        flag = 1;
                        continue;
                }
    }
*/       
        mawb_arr = mawb.split(",");
        for(i = 0; i < mawb_arr.length; ++i) 
        {
                if(mawb_arr[i]=="")
                        continue;
                if($("#"+mawb_arr[i]+"_row").children()[3].textContent=='')
                 {
                        invalid_mawbs += mawb_arr[i] + ",";
                        flag = 1;
                        continue;
                }            
                station = $("#"+mawb_arr[i]+"_row").children()[1].textContent;                
                station_list += station + ",";
             
        }
        station_list= station_list.replace(/ /g,'')

    if(flag==1)
        {
                alert("Consol# fetching must be tried atleast once, before creating the AI file for :\n " + invalid_mawbs);
                return;
        }       
        
        if(username == "" || password == "" )
        {
                alert("Username and password must be enter in Class credential");
                return;
        }       
        if(mawb == "")
        {
                alert("Please select appropiate master whose consol# is missing!");
                return;
        }
//        values = 'username='+username+'&password='+password+'&mawb='+mawb+'&test_update=0';
        values = 'username='+username+'&password='+password+'&mawb='+mawb+'&test_update=0'+'&station_list='+station_list;
        
//        alert(values);

        
        
        $.ajax({
//                url: "http://172.16.15.34:9999/create_ai_file",		// LIVE
                url: "http://172.16.15.34:9090/create_ai_file",		// DEV

                
//                url: "http://172.16.0.109:9010/create_ai_file",		// local		XXX
                
                
                type: "post",
                data: values,
                success: function(msg){
                        alert(msg);
                        
                        $.blockUI.defaults = { 
                                       growlCSS: { 
                                          width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                             
                                },
                },
                $.growlUI('<h1 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+msg+'</h1>');  
                        $("#create_ai_file_container").html("<a href='#' onclick='create_ai_file();'>Create AI File </a>");    
                        
                        
                        $.ajax({
                        	  url: "/process_it/aiLog/",
                        	  type: "POST",
                        	  data: values,
                        	  success: function(msg){
                        		  alert('ai logged')
                        	  }
                        	});       
                   
                        
                        
                        
                        
                        
                },
                beforeSend: function() {
            //alert("The approximate time required to complete this task will be " + (mawb_arr.length*20)/60 + "mins. This task will update the Mawbs in database in background.");
            //"You will get a 'Updated in database!' message upon succesfull completion provided you dont press 'F5','ctrl+F5','Back button'");
                        $("#create_ai_file_container").html("<img title='Consol# fetching in progress!!' src='/static/img/processing.gif'/>")
                        
                }
                   
        });
        

}

function get_consol_no(mawb,username,password)
{
		username = $('#class_uname').val();
        password = $('#class_pass').val();
        mawb = $("#selected_mawb").val();        
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }       
        mawb_arr = mawb.split(",");
        for(i = 0; i < mawb_arr.length - 1; ++i) 
        {
                //if( $("#").val();079-36643342consoleNumber
                //alert(mawb_arr[i] + "=" +$('#'+mawb_arr[i]+"consoleNumber").val());
                //console_number = $('#'+mawb_arr[i]+"consoleNumber").val() //by avinash
                console_number = $("#"+mawb_arr[i]+"_row").children()[3].textContent //by chirag
                if( console_number != "" && console_number != "111111")
                        mawb = mawb.replace(mawb_arr[i]+",","");                                      
        }       
        if(mawb.slice(-1)== ",")
        {
        	mawb = mawb.substring(0, mawb.length - 1);
        }      
        
        if(username == "" || password == "" )
        {
                alert("Username and password must be enter in Class credential");
                return;
        }       
        if(mawb == "")
        {
                alert("Please select appropiate master whose consol#  is missing!");
                return;
        }
        values = 'username='+username+'&password='+password+'&mawb='+mawb+'&test_update=0';
//      alert(values);
//      return;
        $.ajax({

//                url: "http://172.16.15.34:9999/get_console_num",		// LIVE
                  url: "http://172.16.15.34:9090/get_console_num",		// DEV

                  
//                  url: "http://172.16.0.109:9010/get_console_num", 		// XXX	Localhost
        	

                  
//                url: "http://172.16.15.11:9003/get_console_num/",		//XXX		 (for django which replaced cherrypy)
                 
                
                type: "post",
                data: values,
                success: function(msg){ 
                	
                	$("#get_console_container").html("<a href='#' onclick='get_consol_no();'>Get Console # </a>");     
                	  alert(msg);  
                    //    msg= ' MAWB Deleted from here but Exist in the DB...';
                        return growlDoneMsg(msg);
                                      },
                                      
                beforeSend: function() {
         //alert("The approximate time required to complete this task will be " + (mawb_arr.length*20)/60 + "mins. This task will update the Mawbs in database in background.");
                        $("#get_console_container").html("<img title='Console# fetching in progress!!' src='/static/img/processing.gif'/>")                        
                }                  
        });		
}


function clear_selected_mawb(mawb) 
{       
        mawb = $("#selected_mawb").val("");
}

function get_selected_mawb(mawb,username,password)
{       
        alert($("#selected_mawb").val().replace(/\,/g,'\n'));   
}


function update_remarks()
{
	
     	var Digital=new Date();
/*
        var Digital=new Date();
        utc = Digital.getTime() + (Digital.getTimezoneOffset() * 60000);
        nd = new Date(utc + (-8*3600000));
        var pst_hours=nd.getHours();
        var pst_minutes=nd.getMinutes();
        if(pst_minutes < 10)
        {
                pst_minutes = '0'+pst_minutes;
        }
        if(pst_hours < 10)
        {
                pst_hours = '0'+pst_hours;
        } 
*/

    

        username = $('#class_uname').val();
        password = $('#class_pass').val();
        mawb = $("#selected_mawb").val();
        
        if(mawb.slice(-1)== ",")
        {
        	mawb = mawb.substring(0, mawb.length - 1);
        } 
        

        remarks_list = "";
        invalid_mawbs = "";
        console_no = "";
        itinfo= "";
        flag = 0;
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }       
        mawb_arr = mawb.split(",");
            
          
        for(i = 0; i < mawb_arr.length; ++i) 
        {
                if(mawb_arr[i]=="")
                        continue;
                if($("#"+mawb_arr[i]+"_row").children()[3].textContent=='1111111111' || $("#"+mawb_arr[i]+"_row").children()[3].textContent=='')
                {
                        invalid_mawbs += mawb_arr[i] + ",";
                        flag = 1;
                        continue;
                }               
                remark_str = "";                
                mawbNum = $("#"+mawb_arr[i]+"_row").children()[2].textContent;  
                customer = $("#"+mawb_arr[i]+"_row").children()[4].textContent;
                etaDate = $("#"+mawb_arr[i]+"_row").children()[8].textContent;
                etaTime = $("#"+mawb_arr[i]+"_row").children()[9].textContent;
                flightCode = $("#"+mawb_arr[i]+"_row").children()[6].textContent;
                flightNum = $("#"+mawb_arr[i]+"_row").children()[7].textContent;
                slac = $("#"+mawb_arr[i]+"_row").children()[14].textContent;
                pmcOrLoose = $("#"+mawb_arr[i]+"_row").children()[13].textContent;
                chgWeight = $("#"+mawb_arr[i]+"_row").children()[15].textContent;
                remarksInClass = $("#"+mawb_arr[i]+"_row").children()[16].textContent;
                shipmentStatus = $("#"+mawb_arr[i]+"_row").children()[10].textContent;
                speakWith = $("#"+mawb_arr[i]+"_row").children()[12].textContent;
                trackSource = $("#"+mawb_arr[i]+"_row").children()[11].textContent;
                oneFStatus = $("#"+mawb_arr[i]+"_row").children()[17].textContent;
                oneFStatusComment = $("#"+mawb_arr[i]+"_row").children()[21].textContent;
                station = $("#"+mawb_arr[i]+"_row").children()[1].textContent;
//              console_no += $("#"+mawb_arr[i]+"_row").children()[3].textContent + ",";
                part=mawbNum.charAt(mawbNum.length-1 ); 
//                itinfo = $("#"+mawb_arr[i]+"_row").children()[5].textContent;
                
                

            		

                utc = Digital.getTime() + (Digital.getTimezoneOffset() * 60000);
                stationDFW=(station.replace(/\s+/g, ''));

            	if (stationDFW=='DFW')
            	{                
	                nd = new Date(utc + (-5*3600000));
	                var pst_hours=nd.getHours();
	                var pst_minutes=nd.getMinutes();
	                if(pst_minutes < 10)
	                {
	                        pst_minutes = '0'+pst_minutes;
	                }
	                if(pst_hours < 10)
	                {
	                        pst_hours = '0'+pst_hours;
	                }
            	}
            	else{
	                nd = new Date(utc + (-7*3600000));
	                var pst_hours=nd.getHours();
	                var pst_minutes=nd.getMinutes();
	                if(pst_minutes < 10)
	                {
	                        pst_minutes = '0'+pst_minutes;
	                }
	                if(pst_hours < 10)
	                {
	                        pst_hours = '0'+pst_hours;
	                }
            	}
                
                

                  
                if( shipmentStatus=='NB' | shipmentStatus=='NI')
                {
                	 if(etaDate=='')
                     {
                         msg= 'ETA Date is a mandatory field!';
                         return growlErrorMsg(msg);
                     }
                }
                else
                {
                
	                if(etaDate=='')
	                {
	                    msg= 'ETA Date is a mandatory field!';
	                    return growlErrorMsg(msg);
	                }
	                if(etaTime=='')
	                {
	                    msg= 'ETA Time is a mandatory field!';
	                    return growlErrorMsg(msg);
	                }
	                
	                
	             
	                if(flightCode=='')
	                {
	                    msg= 'Flight Code is a mandatory field!';
	                    return growlErrorMsg(msg);
	               
	                    if(flightNum=='')
	                    {
	                    	msg= 'Flight Number is a mandatory field!';
	                    	return growlErrorMsg(msg);
	                    }
	                }
	                
	                if(trackSource=='')
	                {
	                        msg= 'Source is a mandatory field!';
	                        return growlErrorMsg(msg);
	                       
	                }
	                
	                if(isNaN(part))		//	160-66961462A --> 'A' = TRUE
	                	{
	                	if(shipmentStatus=='COB' && slac=='')
	                	{
	                		msg= 'SLAC is a mandatory field!';
	                		return growlErrorMsg(msg);
	                	} 
	                }		
	                	
	                if( shipmentStatus=='')
	                {
	                	msg= 'Shipment Status is a mandatory field!';
	                    return growlErrorMsg(msg);
	                }
	           
                }
                
                
/////////////////////////////////////////////////////////////////////////////// SFO
                
//              if (station == 'SFO ' | station == 'SFO  ' | station == ' SFO' | station == '  SFO' | station == 'SFO' | station == 'SFO   ')
              if (String.trim(station) == 'SFO')
                        {                       
                        if (isNaN(part)) //'Is a CHAR'          [Part A/B]      
                        {                               
                                if(trackSource == 'call' | trackSource == 'CALL')
                                {       
                                        if(shipmentStatus == 'NB' | shipmentStatus == 'nb')
                                        {
                                                remark_str = ' NO BOOKING PER CALL S/W '+speakWith.toUpperCase()+' [Part '+part+']';
                                        }
                                        else if(shipmentStatus == 'NI' | shipmentStatus == 'ni')
                                        {
                                                remark_str = ' NO INFO PER CALL S/W '+speakWith.toUpperCase()+' [Part '+part+']';
                                        }
                                        else if(shipmentStatus == 'BO' | shipmentStatus == 'bo')
                                        {                                               
                                                                                       
                                                        if(etaTime=='')
                                                                remark_str = ' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER CALL ' +speakWith.toUpperCase()+' '+oneFStatusComment+' [Part '+part+']';
                                                        else
                                                                remark_str = ' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER CALL ' +speakWith.toUpperCase()+' '+oneFStatusComment+' [Part '+part+']';
                                                        
                                        }
                                        else if(shipmentStatus == 'COB' | shipmentStatus == 'cob')
                                        {                                                                                               
                                                if(oneFStatusComment == " " | oneFStatusComment == "")
                                                {
                                                        alert("Warning: Please insert details in Comment column !");
                                                        return;
                                                }       
                                                else
                                                        {
                                                if(etaTime=='')
                                                        remark_str = 'COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER CALL ' +speakWith.toUpperCase()+' '+oneFStatusComment+' [Part '+part+']'+' PC-'+slac;
                                                else
                                                        remark_str = 'COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER CALL ' +speakWith.toUpperCase()+' '+oneFStatusComment+' [Part '+part+']'+' PC-'+slac;                                       
                                                        }
                                        }                                               
                                }
                                else if(trackSource == 'web' | trackSource == 'WEB')
                                {       
                                        if(shipmentStatus == 'NB' | shipmentStatus == 'nb')
                                        {
                                                remark_str = ' NO BOOKING PER WEB'+' [Part '+part+']';
                                        }
                                        else if(shipmentStatus == 'NI' | shipmentStatus == 'ni')
                                        {
                                                remark_str = ' NO INFO PER WEB'+' [Part '+part+']';
                                        }
                                        else if(shipmentStatus == 'BO' | shipmentStatus == 'bo')
                                        {
                                               
                                                        if(etaTime=='')
                                                                remark_str = ' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER WEB '+' '+oneFStatusComment+' [Part '+part+']';
                                                        else
                                                                remark_str = ' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER WEB'+' '+oneFStatusComment+' [Part '+part+']';                                       
                                                        
                                        }
                                        else if(shipmentStatus == 'COB' | shipmentStatus == 'cob')
                                        {
                                                if(oneFStatusComment == " " | oneFStatusComment == "")
                                                {
                                                        alert("Warning: Please insert details in comment !");
                                                        return;
                                                }       
                                                else
                                                        {
                                                        if(etaTime=='')
                                                                remark_str = 'COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER WEB'+' '+oneFStatusComment+' [Part '+part+']'+' PC-'+slac;
                                                        else
                                                                remark_str = 'COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER WEB'+' '+oneFStatusComment+' [Part '+part+']'+' PC-'+slac;                                      
                                                        }
                                        }
                                }
                        
                        }       //      [Part A/B       Ends]   
                                                
                        else
                                {
                                        if(trackSource == 'call' | trackSource == 'CALL')
                                        {       
                                                if(shipmentStatus == 'NB' | shipmentStatus == 'nb')
                                                {
                                                        remark_str = ' NO BOOKING PER CALL S/W '+speakWith.toUpperCase();
                                                }
                                                else if(shipmentStatus == 'NI' | shipmentStatus == 'ni')
                                                {
                                                        remark_str = ' NO INFO PER CALL S/W '+speakWith.toUpperCase();
                                                }
                                                else if(shipmentStatus == 'BO' | shipmentStatus == 'bo')
                                                {
                                                      
                
                                                                if(etaTime=='')
                                                                        remark_str = ' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER CALL ' +speakWith.toUpperCase()+' '+oneFStatusComment;
                                                                else
                                                                        remark_str = ' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER CALL ' +speakWith.toUpperCase()+' '+oneFStatusComment;                                           
                                                                
                                                }
                                                else if(shipmentStatus == 'COB' | shipmentStatus == 'cob')
                                                {
                                                        if(oneFStatusComment == " " | oneFStatusComment == "")
                                                        {
                                                                alert("Warning: Please insert details in comment !");
                                                                return;
                                                        }       
                                                        else
                                                                {
                
                                                                if(etaTime=='')
                                                                        remark_str = 'COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER CALL ' +speakWith.toUpperCase()+' '+oneFStatusComment;
                                                                else
                                                                        remark_str = 'COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER CALL ' +speakWith.toUpperCase()+' '+oneFStatusComment;                                          
                                                                }
                                                }                                                       
                                        }
                                        else if(trackSource == 'web' | trackSource == 'WEB')            
                                        {       
                                                if(shipmentStatus == 'NB' | shipmentStatus == 'nb')
                                                {
                                                        remark_str = ' NO BOOKING PER WEB';
                                                }
                                                else if(shipmentStatus == 'NI' | shipmentStatus == 'ni')
                                                {
                                                        remark_str = ' NO INFO PER WEB';
                                                }
                                                else if(shipmentStatus == 'BO' | shipmentStatus == 'bo')
                                                {
                                                       
                                                                if(etaTime=='')
                                                                        remark_str = ' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER WEB'+' '+oneFStatusComment;
                                                                else
                                                                        remark_str = ' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER WEB'+' '+oneFStatusComment;
                                                
                                                }
                                                else if(shipmentStatus == 'COB' | shipmentStatus == 'cob')
                                                {
                                                        if(oneFStatusComment == " " | oneFStatusComment == "")
                                                        {
                                                                alert("Warning: Please insert details in comment !");
                                                                return;
                                                        }       
                                                        else
                                                                {
                
                                                                if(etaTime=='')
                                                                        remark_str = 'COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER WEB'+' '+oneFStatusComment;
                                                                else
                                                                        remark_str = 'COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER WEB'+' '+oneFStatusComment;
                                                
                                                                }
                                                }
                                        }                                       
                                }               
                        }
       
/////////////////////////////////////////////////////////////////////////////// LAX,  etc.                                      
else
        {
                
        if (isNaN(part)) //'Is a CHAR'              [Part A/B]           
        {
                
                if(trackSource == 'call' | trackSource == 'CALL')
                {       
                        if(shipmentStatus == 'NB' | shipmentStatus == 'nb')
                        {
                                remark_str = pst_hours+pst_minutes+' NO BOOKING PER CALL S/W '+speakWith.toUpperCase()+' [Part '+part+']';
                        }
                        else if(shipmentStatus == 'NI' | shipmentStatus == 'ni')
                        {
                                remark_str = pst_hours+pst_minutes+' NO INFO PER CALL S/W '+speakWith.toUpperCase()+' [Part '+part+']';
                        }
                        else if(shipmentStatus == 'BO' | shipmentStatus == 'bo')
                        {
                                if(etaTime=='')
                                        remark_str = pst_hours+pst_minutes+' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER CALL S/W ' +speakWith.toUpperCase()+' [Part '+part+']';
                                else
                                        remark_str = pst_hours+pst_minutes+' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER CALL S/W ' +speakWith.toUpperCase()+' [Part '+part+']';
                        }
                        else if(shipmentStatus == 'COB' | shipmentStatus == 'cob')
                        {
                                if(etaTime=='')
                                        remark_str = pst_hours+pst_minutes+' COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER CALL S/W ' +speakWith.toUpperCase()+' [Part '+part+']'+' PC-'+slac;
                                else
                                        remark_str = pst_hours+pst_minutes+' COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER CALL S/W ' +speakWith.toUpperCase()+' [Part '+part+']'+' PC-'+slac;
                        }
                                
                }
                else if(trackSource == 'web' | trackSource == 'WEB')
                {       
                        if(shipmentStatus == 'NB' | shipmentStatus == 'nb')
                        {
                                remark_str = pst_hours+pst_minutes+' NO BOOKING PER WEB'+' [Part '+part+']';
                        }
                        else if(shipmentStatus == 'NI' | shipmentStatus == 'ni')
                        {
                                remark_str = pst_hours+pst_minutes+' NO INFO PER WEB'+' [Part '+part+']';
                        }
                        else if(shipmentStatus == 'BO' | shipmentStatus == 'bo')
                        {
                                if(etaTime=='')
                                        remark_str = pst_hours+pst_minutes+' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER WEB '+' [Part '+part+']';
                                else
                                        remark_str = pst_hours+pst_minutes+' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER WEB'+' [Part '+part+']';
                        }
                        else if(shipmentStatus == 'COB' | shipmentStatus == 'cob')
                        {
                                if(etaTime=='')
                                        remark_str = pst_hours+pst_minutes+' COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER WEB'+' [Part '+part+']'+' PC-'+slac;
                                else
                                        remark_str = pst_hours+pst_minutes+' COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER WEB'+' [Part '+part+']'+' PC-'+slac;
                        }
                }
        
        }			//		end [Part A/B]      
                
        else
                {
                        if(trackSource == 'call' | trackSource == 'CALL')
                        {       
                                if(shipmentStatus == 'NB' | shipmentStatus == 'nb')
                                {
                                        remark_str = pst_hours+pst_minutes+' NO BOOKING PER CALL S/W '+speakWith.toUpperCase();
                                }
                                else if(shipmentStatus == 'NI' | shipmentStatus == 'ni')
                                {
                                        remark_str = pst_hours+pst_minutes+' NO INFO PER CALL S/W '+speakWith.toUpperCase();
                                }
                                else if(shipmentStatus == 'BO' | shipmentStatus == 'bo')
                                {
                                        if(etaTime=='')
                                                remark_str = pst_hours+pst_minutes+' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER CALL S/W ' +speakWith.toUpperCase();
                                        else
                                                remark_str = pst_hours+pst_minutes+' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER CALL S/W ' +speakWith.toUpperCase();
                                }
                                else if(shipmentStatus == 'COB' | shipmentStatus == 'cob')
                                {
                                        if(etaTime=='')
                                                remark_str = pst_hours+pst_minutes+' COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER CALL S/W ' +speakWith.toUpperCase();
                                        else
                                                remark_str = pst_hours+pst_minutes+' COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER CALL S/W ' +speakWith.toUpperCase();
                                }
                                        
                        }
                        else if(trackSource == 'web' | trackSource == 'WEB')
                        {       
                                if(shipmentStatus == 'NB' | shipmentStatus == 'nb')
                                {
                                        remark_str = pst_hours+pst_minutes+' NO BOOKING PER WEB';
                                }
                                else if(shipmentStatus == 'NI' | shipmentStatus == 'ni')
                                {
                                        remark_str = pst_hours+pst_minutes+' NO INFO PER WEB';
                                }
                                else if(shipmentStatus == 'BO' | shipmentStatus == 'bo')
                                {
                                        if(etaTime=='')
                                                remark_str = pst_hours+pst_minutes+' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER WEB';
                                        else
                                                remark_str = pst_hours+pst_minutes+' BO '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER WEB';
                                }
                                else if(shipmentStatus == 'COB' | shipmentStatus == 'cob')
                                {
                                        if(etaTime=='')
                                                remark_str = pst_hours+pst_minutes+' COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+' PER WEB';
                                        else
                                                remark_str = pst_hours+pst_minutes+' COB '+flightCode+flightNum+'/'+etaDate[3]+etaDate[4]+'@'+etaTime+' PER WEB';
                                }
                        }                       
                }       
        }
                
                var len=remark_str.length;
                if (len >=59)
                        {
                        remark_str=remark_str.split("CALL")
        //              alert("Length= "+len+" *1) "+remark_str[0]+" *2) "+remark_str[1]);
                        console_no += $("#"+mawb_arr[i]+"_row").children()[3].textContent + "," +$("#"+mawb_arr[i]+"_row").children()[3].textContent + ",";
                                                
                        mawb = mawb.replace(mawbNum,mawbNum+','+mawbNum);
        //              alert("M="+mawb+" C="+console_no+" R="+remark_str);
                        remarks_list += remark_str + ",";
                        }
       
                else
                {
                console_no += $("#"+mawb_arr[i]+"_row").children()[3].textContent + ",";
                remarks_list += remark_str + ",";                                               
                }
                
                

 /*
                else
                	{
                	console_no += $("#"+mawb_arr[i]+"_row").children()[3].textContent + ",";
                	if(shipmentStatus == 'COB')
	                {
	             	  itinfo_list= $("#"+mawb_arr[i]+"_row").children()[5].textContent;
	                }
	                else
	                {
	              	  itinfo_list= ""
	                }
	              
	                itinfo += itinfo_list + ",";
                    remarks_list += remark_str + ",";                                               
                    }
                 
*/
                

        }       
        if(flag==1)
        {
                alert("Consol# missing for " + invalid_mawbs);
                return;
        }       
        //alert("===>"+mawb);
        //return;
        if(username == "" || password == "" )
        {
                alert("Username and password must be enter in Class credential");
                return;
        }       
        if(mawb == "")
        {
                alert("Please select appropiate master whose consol# is missing!");
                return;
        }
  

      values = 'username='+username+'&password='+password+'&console_no='+ console_no  +'&mawb='+mawb+'&test_update=0'+'&remark='+remarks_list ;        
//        values = 'username='+username+'&password='+password+'&console_no='+ console_no  +'&mawb='+mawb+'&test_update=0'+'&itinfo='+itinfo+'&remark='+remarks_list ;
        
//      alert("M="+mawb+" C="+ console_no + " R =  "+remarks_list);          //XXX
//      alert(values);          //XXX
//      return;
      
        $.ajax({
//            url: "http://172.16.15.34:9999/update_remarks", 		// LIVE        	
            url: "http://172.16.15.34:9090/update_remarks", 		// DEV      to be--

//            url: "http://172.16.14.143:9010/update_remarks", 		// XXX	Localhost
         
                type: "post",
                data: values,
                success: function(msg){
                        alert(msg);

                        $.blockUI.defaults = { 
                                       growlCSS: { 
                                          width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                             
                                },
                },
                $.growlUI('<h3 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+msg+'</h3>');  
                        
                        $("#update_remarks_container").html("<a href='#' onclick='update_remarks();'>Update Remarks</a>");              
                },
                beforeSend: function() {
                        $("#update_remarks_container").html("<img title='Remarks updation in progress!!' src='/static/img/processing.gif'/>")
                        
                }
        });             
}




function itinfo_to_class()
{

        username = $('#class_uname').val();
        password = $('#class_pass').val();
        mawb = $("#selected_mawb").val();
        
        if(mawb.slice(-1)== ",")
        {
        	mawb = mawb.substring(0, mawb.length - 1);
        } 
        

        itinfo_list = "";
        invalid_mawbs = "";
        console_no = "";
        itinfo= "";
        flag = 0;
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }       
        mawb_arr = mawb.split(",");
            
          
        for(i = 0; i < mawb_arr.length; ++i) 
        {
                if(mawb_arr[i]=="")
                        continue;
                if($("#"+mawb_arr[i]+"_row").children()[3].textContent=='1111111111' || $("#"+mawb_arr[i]+"_row").children()[3].textContent=='')
                {
                        invalid_mawbs += mawb_arr[i] + ",";
                        flag = 1;
                        continue;
                }               
                remark_str = "";                
                mawbNum = $("#"+mawb_arr[i]+"_row").children()[2].textContent;  
                customer = $("#"+mawb_arr[i]+"_row").children()[4].textContent;
                etaDate = $("#"+mawb_arr[i]+"_row").children()[8].textContent;
                etaTime = $("#"+mawb_arr[i]+"_row").children()[9].textContent;
                flightCode = $("#"+mawb_arr[i]+"_row").children()[6].textContent;
                flightNum = $("#"+mawb_arr[i]+"_row").children()[7].textContent;
                slac = $("#"+mawb_arr[i]+"_row").children()[14].textContent;
                pmcOrLoose = $("#"+mawb_arr[i]+"_row").children()[13].textContent;
                chgWeight = $("#"+mawb_arr[i]+"_row").children()[15].textContent;
                remarksInClass = $("#"+mawb_arr[i]+"_row").children()[16].textContent;
                shipmentStatus = $("#"+mawb_arr[i]+"_row").children()[10].textContent;
                speakWith = $("#"+mawb_arr[i]+"_row").children()[12].textContent;
                trackSource = $("#"+mawb_arr[i]+"_row").children()[11].textContent;
                oneFStatus = $("#"+mawb_arr[i]+"_row").children()[17].textContent;
                oneFStatusComment = $("#"+mawb_arr[i]+"_row").children()[21].textContent;
                station = $("#"+mawb_arr[i]+"_row").children()[1].textContent;
                console = $("#"+mawb_arr[i]+"_row").children()[3].textContent;
                part=mawbNum.charAt(mawbNum.length-1 ); 
                itinfo = $("#"+mawb_arr[i]+"_row").children()[5].textContent;
              
                  
                if( shipmentStatus=='NB' | shipmentStatus=='NI')
                {
                	 if(etaDate=='')
                     {
                         msg= 'ETA Date is a mandatory field!';
                         return growlErrorMsg(msg);
                     }
                }
                else
                {
	                if(etaDate=='')
	                {
	                    msg= 'ETA Date is a mandatory field!';
	                    return growlErrorMsg(msg);
	                }
	                if(etaTime=='')
	                {
	                    msg= 'ETA Time is a mandatory field!';
	                    return growlErrorMsg(msg);
	                }
	             
	                if(flightCode=='')
	                {
	                    msg= 'Flight Code is a mandatory field!';
	                    return growlErrorMsg(msg);
	               
	                    if(flightNum=='')
	                    {
	                    	msg= 'Flight Number is a mandatory field!';
	                    	return growlErrorMsg(msg);
	                    }
	                }
                }
                	console_no +=console  + ",";
                	if(shipmentStatus == 'COB')
	                {
//	             	 itinfo= $("#"+mawb_arr[i]+"_row").children()[5].textContent;
	             	 itinfo_list += itinfo + ",";
	                }
	                else
	                {
	                	alert("Shipment status should be COB");
	                	return;	              		  
	                }
        }    
    
        if(flag==1)
        {
                alert("Consol# missing for " + invalid_mawbs);
                return;
        }       

        if(username == "" || password == "" )
        {
                alert("Username and password must be enter in Class credential");
                return;
        }       
        if(mawb == "")
        {
                alert("Please select appropiate master whose consol# is missing!");
                return;
        }
      values = 'username='+username+'&password='+password+'&console_no='+ console_no  +'&mawb='+mawb+'&test_update=0'+'&remark='+itinfo_list ;        
       
//      alert(values);          //XXX
//      return;
      
        $.ajax({
//            url: "http://172.16.15.34:9999/update_remarks", 		// LIVE        	
            url: "http://172.16.15.34:9090/update_remarks", 		// DEV      to be--

//            url: "http://172.16.0.109:9010/update_remarks", 		// XXX	Localhost
         
                type: "post",
                data: values,
                success: function(msg){
                        alert(msg);

                        $.blockUI.defaults = { 
                                       growlCSS: { 
                                          width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                             
                                },
                },
                $.growlUI('<h3 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+msg+'</h3>');  
                        
                        $("#update_it_info").html("<a href='#' onclick='itinfo_to_class();'>IT Info to CLASS</a>");              
                },
                beforeSend: function() {
                        $("#update_it_info").html("<img title='Remarks updation in progress!!' src='/static/img/processing.gif'/>")
                        
                }
        });             
}



function hawb_count()
{

        username = $('#class_uname').val();
        password = $('#class_pass').val();
        mawb = $("#selected_mawb").val();
        
        if(mawb.slice(-1)== ",")
        {
        	mawb = mawb.substring(0, mawb.length - 1);
        } 
        
        console_list = "";
        invalid_mawbs = "";
        flag = 0;
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }       
        mawb_arr = mawb.split(",");
          
        for(i = 0; i < mawb_arr.length; ++i) 
        {
                if(mawb_arr[i]=="")
                        continue;
                if($("#"+mawb_arr[i]+"_row").children()[3].textContent=='1111111111' || $("#"+mawb_arr[i]+"_row").children()[3].textContent=='')
                {
                        invalid_mawbs += mawb_arr[i] + ",";
                        flag = 1;
                        continue;
                }               
                remark_str = "";                
                mawbNum = $("#"+mawb_arr[i]+"_row").children()[2].textContent;  
                customer = $("#"+mawb_arr[i]+"_row").children()[4].textContent;
                etaDate = $("#"+mawb_arr[i]+"_row").children()[8].textContent;
                etaTime = $("#"+mawb_arr[i]+"_row").children()[9].textContent;
                flightCode = $("#"+mawb_arr[i]+"_row").children()[6].textContent;
                flightNum = $("#"+mawb_arr[i]+"_row").children()[7].textContent;
                slac = $("#"+mawb_arr[i]+"_row").children()[14].textContent;
                pmcOrLoose = $("#"+mawb_arr[i]+"_row").children()[13].textContent;
                chgWeight = $("#"+mawb_arr[i]+"_row").children()[15].textContent;
                remarksInClass = $("#"+mawb_arr[i]+"_row").children()[16].textContent;
                shipmentStatus = $("#"+mawb_arr[i]+"_row").children()[10].textContent;
                speakWith = $("#"+mawb_arr[i]+"_row").children()[12].textContent;
                trackSource = $("#"+mawb_arr[i]+"_row").children()[11].textContent;
                oneFStatus = $("#"+mawb_arr[i]+"_row").children()[17].textContent;
                oneFStatusComment = $("#"+mawb_arr[i]+"_row").children()[21].textContent;
                station = $("#"+mawb_arr[i]+"_row").children()[1].textContent;
//              console_no += $("#"+mawb_arr[i]+"_row").children()[3].textContent + ",";
                part=mawbNum.charAt(mawbNum.length-1 ); 
//                itinfo = $("#"+mawb_arr[i]+"_row").children()[5].textContent;
                console_no = $("#"+mawb_arr[i]+"_row").children()[3].textContent;
                
                console_list +=console_no + ",";
            
        }
        
        
        if(console_list == "")
        {
                alert("Console Number is a mandatory field!");
                return;
        }


        if ( console_list.indexOf("111111") != -1 )
        {
        	alert("Please uncheck Masters with Console='111111' ");
        	return;
        }

        
        if(flag==1)
        {
                alert("Consol# missing for " + invalid_mawbs);
                return;
        }       

        if(username == "" || password == "" )
        {
                alert("Username and password must be enter in Class credential");
                return;
        }       
        if(mawb == "")
        {
                alert("Please select appropiate master whose consol# is missing!");
                return;
        }
  
      values = 'username='+username+'&password='+password+'&console_no='+ console_list  +'&mawb='+mawb+'&test_update=0' ;        
        
//      alert("M="+mawb+" C="+ console_no + " R =  "+remarks_list);          //XXX
//      alert(values);          //XXX
//      return;
      
        $.ajax({

//            url: "http://172.16.15.34:9999/hawb_count", 		// LIVE
            url: "http://172.16.15.34:9090/hawb_count", 		// DEV
            
//            url: "http://172.16.0.109:9010/hawb_count", 		// XXX	Localhost
         
                type: "post",
                data: values,
                success: function(msg){
                        alert(msg);

                        $.blockUI.defaults = { 
                                       growlCSS: { 
                                          width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                             
                                },
                },
                $.growlUI('<h3 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+msg+'</h3>');  
                        
                        $("#hawb_count").html("<a href='#' onclick='hawb_count();'>HAWB Count</a>");              
                },
                beforeSend: function() {
                        $("#hawb_count").html("<img title='HBL Count in progress!!' src='/static/img/processing.gif'/>")
                        
                }
        });             
}



















function fnb_process(sendStation,requestFrom)
{

        username = $('#class_uname').val();
        password = $('#class_pass').val();
        mawb = $("#selected_mawb").val();
        if(mawb.slice(-1)== ",")
        {
        	mawb = mawb.substring(0, mawb.length - 1);
        } 
        console_list = "";
        invalid_mawbs = "";
        process_status = "";
        flag = 0;
        cc="";
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }       
        mawb_arr = mawb.split(",");
        for(i = 0; i < mawb_arr.length; ++i) 
        {
                if(mawb_arr[i]=="")
                        continue;
                if($("#"+mawb_arr[i]+"_row").children()[3].textContent=='1111111111' || $("#"+mawb_arr[i]+"_row").children()[3].textContent=='')
                {
                        invalid_mawbs += mawb_arr[i] + ",";
                        flag = 1;
                        continue;
                }               
                remark_str = "";                
                mawbNum = $("#"+mawb_arr[i]+"_row").children()[2].textContent;  
                station = $("#"+mawb_arr[i]+"_row").children()[1].textContent;

                part=mawbNum.charAt(mawbNum.length-1 ); 
             
                if (requestFrom=="master"){
                	console_no=document.getElementById(mawb_arr[i]+'_consoleNumber').value;
                	console_list+=console_no + ",";
                	process=document.getElementById(mawb_arr[i]+'_spProStatus').value;
                    process_status += process;

                }
                else{
                    console_no = $("#"+mawb_arr[i]+"_row").children()[3].textContent;
                    console_list +=console_no + ",";   
                    process = $("#"+mawb_arr[i]+"_row").children()[22].textContent;
                    process_status += process;
                }
                
        }
        if(console_list == "")
        {
                alert("Console Number is a mandatory field!");
                return;
        }
        if ( console_list.indexOf("111111") != -1 )
        {
        	alert("Please uncheck Masters with Console='111111' ");
        	return;
        }
        if(flag==1)
        {
                alert("Consol# missing for " + invalid_mawbs);
                return;
        }       
        if(username == "" || password == "" )
        {
                alert("Username and password must be enter in Class credential");
                return;
        } 
        
        if(mawb == "")
        {
                alert("Please select appropiate master whose consol# is missing!");
                return;
        }
        
        //if(process_status.search("Processed") != -1)
        if(process_status == "Processed")
        {
                alert("Please Unselect master whose FNB Status is Fetched ..!");
                return;
        }
  
        if(sendStation.replace(/\s+/g, ' ')=="DFW")
        	{
        		values = 'username='+username+'&password='+password+'&console_no='+ console_list  +'&mawb='+mawb+'&test_update=0'+'&sendStation='+'DFW' ; 
        	}
        else 
        	{
        		values = 'username='+username+'&password='+password+'&console_no='+ console_list  +'&mawb='+mawb+'&test_update=0'+'&sendStation='+'LAX';
        	}
             
//      alert(values);          //XXX
//      return;
      
        $.ajax({

//            url: "http://172.16.15.34:9999/fnb_process",
            url: "http://172.16.15.34:9090/fnb_process", 		// DEV
            
//            url: "http://172.16.0.109:9010/fnb_process", 		// XXX	Localhost
                    
                type: "post",
                data: values,
                success: function(msg){
                        alert(msg);
                        $.blockUI.defaults = { 
                                       growlCSS: { 
                                          width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                             
                                },
                },
                $.growlUI('<h3 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+msg+'</h3>');  
                        
                        //$("#fnb_process_status").html("<a href='#' >FNB Process</a>");              
                },
                beforeSend: function() {
                    $.growlUI('<h3 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">Please wait till FNB Process<br> Status is Fetched...</h3>');  
                       // $("#fnb_process_status").html("<img title='FNB in progress!!' src='/static/img/processing.gif'/>")   
                }
        });             
}


function fetch_flightEta()
{
        username = $('#class_uname').val();
        password = $('#class_pass').val();
        mawb = $("#selected_mawb").val();
        if(mawb.slice(-1)== ",")
        {
        	mawb = mawb.substring(0, mawb.length - 1);
        } 
        console_list = "";
        invalid_mawbs = "";
        flag = 0;

        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }       
        mawb_arr = mawb.split(",");
        for(i = 0; i < mawb_arr.length; ++i) 
        {
                if(mawb_arr[i]=="")
                        continue;
                if($("#"+mawb_arr[i]+"_row").children()[3].textContent=='1111111111' || $("#"+mawb_arr[i]+"_row").children()[3].textContent=='')
                {
                        invalid_mawbs += mawb_arr[i] + ",";
                        flag = 1;
                        continue;
                }                    

                console_no = $("#"+mawb_arr[i]+"_row").children()[3].textContent;
                console_list +=console_no + ",";                

        }
        if(console_list == "")
        {
                alert("Console Number is a mandatory field!");
                return;
        }
        if ( console_list.indexOf("111111") != -1 )
        {
        	alert("Please uncheck Masters with Console='111111' ");
        	return;
        }
        if(flag==1)
        {
                alert("Consol# missing for " + invalid_mawbs);
                return;
        }       
        if(username == "" || password == "" )
        {
                alert("Username and password must be enter in Class credential");
                return;
        }       
        if(mawb == "")
        {
                alert("Please select appropiate master whose consol# is missing!");
                return;
        }
        
      values = 'username='+username+'&password='+password+'&console_no='+ console_list  +'&mawb='+mawb+'&test_update=0' ;  
//      alert(values);          //XXX
//      return;      
        $.ajax({

//            url: "http://172.16.15.34:9999/fetch_flightEta", 		// live        	
            url: "http://172.16.15.34:9090/fetch_flightEta", 		// DEV

//            url: "http://172.16.0.109:9010/fetch_flightEta", 		// XXX	Localhost
         
                type: "post",
                data: values,
                success: function(msg){
                        alert(msg);
                        $.blockUI.defaults = { 
                                       growlCSS: { 
                                          width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                             
                                },
                },
                $.growlUI('<h3 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+msg+'</h3>');  
                        
                        $("#fetch_flightEta").html("<a href='#' onclick='fetch_flightEta();'>Fetch Flight and ETA</a>");              
                },
                beforeSend: function() {
                        $("#fetch_flightEta").html("<img title='FNB in progress!!' src='/static/img/processing.gif'/>")   
                }
        });             
}





























function master_wright(des_station)
{

        username = $('#class_uname').val();
        password = $('#class_pass').val();
        mawb = $("#selected_mawb").val();
        
        if(mawb.slice(-1)== ",")
        {
        	mawb = mawb.substring(0, mawb.length - 1);
        } 
        

        


        itinfo_list = "";
        invalid_mawbs = "";
        console_no = "";
        
    	flightCode_list="";
    	flightNum_list ="";
    	etaDate_list ="";
        etaTime_list ="";
        station_list="";
               
        
        itinfo= "";
        flag = 0;
        if(mawb == "")
        {
                alert("No Master selected!");
                return;
        }       
        mawb_arr = mawb.split(",");
            
        
        
        for(i = 0; i < mawb_arr.length; ++i) 
        {
                if(mawb_arr[i]=="")
                        continue;
                if($("#"+mawb_arr[i]+"_row").children()[3].textContent=='1111111111' || $("#"+mawb_arr[i]+"_row").children()[3].textContent=='')
                {
                        invalid_mawbs += mawb_arr[i] + ",";
                        flag = 1;
                        continue;
                }               
                remark_str = "";                
                mawbNum = $("#"+mawb_arr[i]+"_row").children()[2].textContent;  

                etaDate = $("#"+mawb_arr[i]+"_row").children()[8].textContent;
                etaTime = $("#"+mawb_arr[i]+"_row").children()[9].textContent;
                
                flightCode = $("#"+mawb_arr[i]+"_row").children()[6].textContent;
                flightNum = $("#"+mawb_arr[i]+"_row").children()[7].textContent;

                shipmentStatus = $("#"+mawb_arr[i]+"_row").children()[10].textContent;

                station = $("#"+mawb_arr[i]+"_row").children()[1].textContent;
                station_list += station;
                
                console = $("#"+mawb_arr[i]+"_row").children()[3].textContent;

              

                if((station_list.replace(/^\s+|\s+$/g,'')).search("IAH") != -1)
            	{
                	if((station_list.replace(/^\s+|\s+$/g,'')).search("DFW") != -1)
                		{
                		alert("Please check the Station Selected, Only one Station allowed at a time..!");
                		return;
                		}
                	else{
                    	des_station="IAH";
                		}
            	}
    	

	                if(etaDate=='')
	                {
	                    msg= 'ETA Date is a mandatory field!';
	                    return growlErrorMsg(msg);
	                }
	                if(etaTime=='')
	                {
	                    msg= 'ETA Time is a mandatory field!';
	                    return growlErrorMsg(msg);
	                }
	             
	                if(flightCode=='')
	                {
	                    msg= 'Flight Code is a mandatory field!';
	                    return growlErrorMsg(msg);
	               
	                    if(flightNum=='')
	                    {
	                    	msg= 'Flight Number is a mandatory field!';
	                    	return growlErrorMsg(msg);
	                    }
	                }
                
                	console_no +=console  + ",";
                	flightCode_list += flightCode + ",";
                	flightNum_list += flightNum + ",";
                	etaDate_list += etaDate + ",";
                    etaTime_list += etaTime + ",";

                	
        }    
    
        if(flag==1)
        {
                alert("Consol# missing for " + invalid_mawbs);
                return;
        }       

        if(username == "" || password == "" )
        {
                alert("Username and password must be enter in Class credential");
                return;
        }       
        if(mawb == "")
        {
                alert("Please select appropiate master whose consol# is missing!");
                return;
        }
        
        
        
        
values = 'username='+username+'&password='+password+'&console_no='+console_no+'&mawb='+mawb+'&test_update=0'+'&flightCode='+flightCode_list+'&flightNum='+flightNum_list+'&etaDate='+etaDate_list+'&etaTime='+etaTime_list+'&des_station='+des_station ;        
       
//      alert(values);          //XXX
//      return;
      
        $.ajax({
             	
 //           url: "http://172.16.15.34:9999/master_wright", 		//Live
            url: "http://172.16.15.34:9090/master_wright", 	 				// DEV 

         
                type: "post",
                data: values,
                success: function(msg){
                        alert(msg);

                        $.blockUI.defaults = { 
                                       growlCSS: { 
                                          width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                             
                                },
                },
                $.growlUI('<h3 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+msg+'</h3>');  
                        
               //         $("#master_wright").html("<a href='#' onclick='master_wright("+des_station+");'>Master Screen Update</a>");  
                        $("#master_wright").html('<a href="#" onclick="master_wright(\''+des_station+'\');">Master Screen Update</a>');
                },
                beforeSend: function() {
                        $("#master_wright").html("<img title='Remarks updation in progress!!' src='/static/img/processing.gif'/>")
                        
                }
        });             
}






































function update_dispatch()
{      
        var Digital=new Date();
        utc = Digital.getTime() + (Digital.getTimezoneOffset() * 60000);
        nd = new Date(utc + (-8*3600000));
        var pst_hours=nd.getHours();
        var pst_minutes=nd.getMinutes();
        if(pst_minutes < 10)
        {
                pst_minutes = '0'+pst_minutes;
        }
        if(pst_hours < 10)
        {
                pst_hours = '0'+pst_hours;
        }

        var dispatch_type= "";
        var dispatch_str = "";
                        
        if($('input:radio[name=dispatch_type]:checked').val())
        { 
                dispatch_type = $('input:radio[name=dispatch_type]:checked').val();
        }
        else{
                alert('Warnning: Select the Dispatch Type !');
                return;
        }
        username = $('#class_uname').val();
        password = $('#class_pass').val();
        mawb = $("#selected_mawb").val();
        
        
        invalid_mawbs = "";
        console_no = "";

        flag = 0;
        if(mawb == "")
        {
                alert("No Master selected !");
                return;
        }       
        mawb_arr = mawb.split(",");
        
        for(i = 0; i < mawb_arr.length; ++i) 
        {
                if(mawb_arr[i]=="")
                        continue;
                if($("#"+mawb_arr[i]+"_row").children()[3].textContent=='111111' || $("#"+mawb_arr[i]+"_row").children()[3].textContent=='')
                {
                        invalid_mawbs += mawb_arr[i] + ",";
                        flag = 1;
                        continue;
                }               
                remark_str = "";
                console_no += $("#"+mawb_arr[i]+"_row").children()[3].textContent + ",";                
                mawbNum = $("#"+mawb_arr[i]+"_row").children()[2].textContent;  
                dispatch_str += pst_hours.toString()+ pst_minutes.toString() +" DISPATCHED "+ dispatch_type.toUpperCase()+",";
        }       
        if(flag==1)
        {
                alert("Consol# missing for " + invalid_mawbs);
                return;
        }       

        if(username == "" || password == "" )
        {
                alert("Username and password must be enter in Class credential");
                return;
        }       
        if(mawb == "")
        {
                alert("Please select appropiate master whose consol# is missing!");
                return;
        }
        values = 'username='+username+'&password='+password+'&console_no='+ console_no  +'&mawb='+mawb+'&test_update=0'+'&remark='+dispatch_str;

        $.ajax({
//            url: "http://172.16.15.34:9999/update_remarks",	 				// LIVE             
              url: "http://172.16.15.34:9090/update_remarks",	 				// DEV 
              
//              url: "http://172.16.0.109:9010/update_remarks", 		// XXX	Localhost
              
//            url: "http://172.16.15.11:9999/update_remarks/",           //  XXX  (for django which replaced cherrypy)

                type: "post",
                data: values,
                success: function(msg){
                        alert(msg);                       
                        
                        $.blockUI.defaults = { 
                                       growlCSS: { 
                                          width:'450px', top:'100px', left:'', right:'20px', border:'none',padding:'5px',opacity:0.8,cursor:null, color:'#fff', backgroundColor:'#000',                                                             
                                },
                },
                $.growlUI('<h3 style="width:450px;top:100px;left:;right:px;color:white; padding: 15px 15px 15px 15px;text-align: left;margin-top: 100px; ">'+msg+'</h3>');  

                        $("#update_dispatch").html("Update Dispatch");          
                },
                beforeSend: function() {
                        $("#update_dispatch").html("<img title='Dispatch updation in progress!!' src='/static/img/processing.gif'/>")
                        
                }
        });             

}


        
function validatefilter()
{
        
        date_regex = /^(0[1-9]|1[012])[- . \/](0[1-9]|[12][0-9]|3[01])[- .\/]\d\d$/;
        time_regex = /^(0[0-9][0-5][0-9]|1[0-9][0-5][0-9]|2[0-3][0-5][0-9])$/;
        
        var consoleNumber = $('#consoleNumberFilter').val();
        var slac = $('#slacFilter').val();
        var chgWeight = $('#chgWeightFilter').val();
        var flightNum = $('#flightNumFilter').val();
        var etaDateFrom = $('#etaDateFromFilter').val();
        var etaDateTo = $('#etaDateToFilter').val();
        var etaTimeFrom = $('#etaTimeFromFilter').val();
        var etaTimeTo = $('#etaTimeToFilter').val();
        var lastUpdatedDateFrom = $('#lastUpdatedDateFromFilter').val();
        var lastUpdatedDateTo = $('#lastUpdatedDateToFilter').val();
        var lastUpdatedTimeFrom = $('#lastUpdatedTimeFromFilter').val();
        var lastUpdatedTimeTo = $('#lastUpdatedTimeToFilter').val();
        
        
        if(consoleNumber != '...' && consoleNumber != '' && isNaN(consoleNumber))
        {
                alert(consoleNumber);
                alert('Consol should be a number!');            
                return false;
        }
        
        if(slac != '...' && slac != '' && isNaN(slac))
        {
                alert('SLAC should be a number!');              
                return false;
        }
        
        if(chgWeight != '...' && chgWeight != '' && isNaN(chgWeight))
        {
                alert('CHG. WGHT. should be a number!');                
                return false;
        }
        
        if(etaDateFrom.search(date_regex) == -1 && etaDateFrom != '' && etaDateFrom != '9999')
        {
                alert('ETA Date From must have mm-dd-yy format!!');             
                return false;
        }
        if(etaDateTo.search(date_regex) == -1 && etaDateTo != '' && etaDateTo != '9999')
        {
                alert('ETA Date To must have mm-dd-yy format!!');               
                return false;
        }
        if(etaTimeFrom.search(time_regex) == -1 && etaTimeFrom != '' && etaTimeFrom != '...')
        {
                alert('ETA Time From must have hhmm (0000-2359) format!!');             
                return false;                   
        }
        if(etaTimeTo.search(time_regex) == -1 && etaTimeTo != '' && etaTimeTo != '...')
        {
                alert('ETA Time To must have hhmm (0000-2359) format!!');               
                return false;                   
        }       
        if(lastUpdatedDateFrom.search(date_regex) == -1 && lastUpdatedDateFrom != '' && lastUpdatedDateFrom != '9999')
        {
                alert('Last Update From Date must have mm-dd-yy format!!');             
                return false;
        }
        
        if(lastUpdatedDateTo.search(date_regex) == -1 && lastUpdatedDateTo != '' && lastUpdatedDateTo != '9999')
        {
                alert('Last Update Date To must have mm-dd-yy format!!');               
                return false;
        }
        if(lastUpdatedTimeFrom.search(time_regex) == -1 && lastUpdatedTimeFrom != '' && lastUpdatedTimeFrom != '...')
        {
                alert('Last Updated Time From must have hhmm (0000-2359) format!!');            
                return false;   
        }
        if(lastUpdatedTimeTo.search(time_regex) == -1 && lastUpdatedTimeTo != '' && lastUpdatedTimeTo != '...')
        {
                alert('Last Updated Time To must have hhmm (0000-2359) format!!');              
                return false;   
        }
        else
        {
                return true;
        }
}

function validatefiltermaster()
{
        
        date_regex = /^(0[1-9]|1[012])[- . \/](0[1-9]|[12][0-9]|3[01])[- .\/]\d\d$/;
        time_regex = /^(0[0-9][0-5][0-9]|1[0-9][0-5][0-9]|2[0-3][0-5][0-9])$/;
        
        var consoleNumber = $('#consoleNumberFilter').val();
        var slac = $('#slacFilter').val();
        var chgWeight = $('#chgWeightFilter').val();
        var flightNum = $('#flightNumFilter').val();
        var etaDateFrom = $('#etaDateFromFilter').val();
        var etaDateTo = $('#etaDateToFilter').val();
        var cobDateFrom = $('#cobDateFromFilter').val();
        var cobDateTo = $('#cobDateToFilter').val();
        var etaTimeFrom = $('#etaTimeFromFilter').val();
        var etaTimeTo = $('#etaTimeToFilter').val();
        
        
        if(consoleNumber != '...' && consoleNumber != '' && isNaN(consoleNumber))
        {
                alert(consoleNumber);
                alert('Consol should be a number!');            
                return false;
        }
        
        if(slac != '...' && slac != '' && isNaN(slac))
        {
                alert('SLAC should be a number!');
                return false;
        }
        
        if(chgWeight != '...' && chgWeight != '' && isNaN(chgWeight))
        {
                alert('CHG. WGHT. should be a number!');
                return false;
        }
        
        if(etaDateFrom.search(date_regex) == -1 && etaDateFrom != '' && etaDateFrom != '9999')
        {
                alert('ETA Date From must have mm-dd-yy format!!');             
                return false;
        }
        if(etaDateTo.search(date_regex) == -1 && etaDateTo != '' && etaDateTo != '9999')
        {
                alert('ETA Date To must have mm-dd-yy format!!');               
                return false;
        }
        if(etaDateFrom.search(date_regex) == -1 && etaDateFrom != '' && etaDateFrom != '9999')
        {
                alert('ETA Date From must have mm-dd-yy format!!');             
                return false;
        }
        if(etaDateTo.search(date_regex) == -1 && etaDateTo != '' && etaDateTo != '9999')
        {
                alert('ETA Date To must have mm-dd-yy format!!');               
                return false;
        }
        if(cobDateFrom.search(date_regex) == -1 && cobDateFrom != '' && cobDateFrom != '9999')
        {
                alert('ETA Date From must have mm-dd-yy format!!');             
                return false;
        }
        if(cobDateTo.search(date_regex) == -1 && cobDateTo != '' && cobDateTo != '9999')
        {
                alert('ETA Date To must have mm-dd-yy format!!');               
                return false;
        }
        
        else
        {
                return true;
        }
}

function movebacktopap(mbl_id)
{
        ajaxWithSerialize('n','processingStatus','/process_it/mawbAction/','actionType=movebacktopap&mawb_id='+mbl_id);
        $('#'+mbl_id+'_row').css('display','None');
}

function deleteone(mbl_id)
{
        var answer = confirm("Please confirm the deletion of record!!");
        if (answer){
                ajaxWithSerialize('n','processingStatus','/process_it/mawbAction/','actionType=delete&mawb_id='+mbl_id);
                $('#'+mbl_id+'_row').css('display','None');
        }
        else{
                return false;           
        }
        
}

function chkhasmawb(id,chkmawb)
{               
        
        mawb_regex = /^(\d\d\d-\d\d\d\d\d\d\d\d|\d\d\d-\d\d\d\d\d\d\d\d([A-L]))$/;
        var formdict = 'id='+id+'&chkmawb='+chkmawb;
        if(chkmawb.search(mawb_regex) == -1)
        {               
                alert('Master # should consist of ddd-ddddddddC format. Here all "d" are digits & "C" is any capital character between A-L or nothing, eg. 123-23342312A or 123-12345678!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        else
        {               
                $.ajax({
                url: "/process_it/chkHasMawb/",
                type: "post",
                data: formdict,
                success: function(resp_list){
                    console.log(resp_list);
//                        $.each(resp_list, function(key,val){

                            if(resp_list.key == 1){
                                if(resp_list.papFlag == true) {
                                    $('#load_resp').html("<img src='/static/img/done.gif' title='Mawb exist in database!' /><h3 style='color: blue'>Master visible in Pre-Alert Processing Sheet</h3>");
                                    msg = "Mawb exist in database!";
                                    return growlDoneMsg(msg);
                                }
                                else if(resp_list.papFlag == false) {
                                    $('#load_resp').html("<img src='/static/img/done.gif' title='Mawb exist in database!' /><h3 style='color: red'>Master NOT visible in Pre-Alert Processing Sheet</h3>");
                                    msg = "Mawb exist in database!";
                                    return growlDoneMsg(msg);
                                }
                            }
                            else if(resp_list.key == 0){
                                    $('#load_resp').html("<img src='/static/img/error.gif' title='Mawb does not exist in database!, hence added but without station' />");
                                    msg="Mawb does not exist in database!, hence added but without station..";
                                    return growlErrorMsg(msg);
                            }
//                        });
                },
                beforeSend: function() {                
                        $('#load_resp').html("<img src='/static/img/processing.gif' />");
                }
            });
        }
}

function IsEnterKey(e)
{
        if(e) {
                if (e.keyCode == 13) return true;
                else 
                {
                        /*
                        var child_trs = $("#dataTable tbody")[0].children;
                        $.each(child_trs, function(i) {
                            if(this.id.search('_row') != -1)
                            {                                   
                                child_tds = $('#'+this.id+' td').children();                            
                                
                                        $.each(child_tds, function(i){
                                                
                                                if(this.id.search('mawbNum')!=-1)
                                                        {
                                                                alert(this.id);                         
                                                        }
                                                
                                        });
                                        //mbl_id = $('#'+this.id+' td')[4].children[0].id;                                                                              
                            }                                   
                        });
                        */                                              
                }
        }
        else
        {
                //alert('------'+e.keyCode);
                return false;
        }
}

function new_track_mawb(mawb)
{
        var first_parent_tr = $('#'+mawb+'_update').parent().parent();
        first_parent_tr.children('.mawbNum').css("background-color","#FCA1A1");
        var pageURL='http://www.trackload.com/cgi-bin/rapidtrk.cgi?MAWB=';
        if(mawb!='')
        {
                //if(mawb)
                        //window.open (pageURL+mawb, 'xxx', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=1000, height=500, top=60, left=100');
                window.open (pageURL+mawb, 'xxx', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=no, copyhistory=no, width=1000, height=500, top=60, left=100');
                //else
                        //window.open (pageURL+mawb, 'xxx', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=1000, height=500, top=60, left=100');           
        }
        else
        {
                alert('Master not found for this entry! cant track');
        }
        //window.open (pageURL+, title, 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=500, height=300, top=60, left=100');
        
}

function track_mawb(mawb)
{
        
        $('#'+mawb+'mawbNum').css("background-color","#FCA1A1");
        $('#'+mawb+'flightCode').focus();
        var pageURL='http://www.trackload.com/cgi-bin/rapidtrk.cgi?MAWB=';
        if(mawb!='')
        {
                //if(mawb)
                        //window.open (pageURL+mawb, 'xxx', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=1000, height=500, top=60, left=100');
                window.open (pageURL+mawb, 'xxx', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=no, copyhistory=no, width=1000, height=500, top=60, left=100');
                //else
                        //window.open (pageURL+mawb, 'xxx', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=1000, height=500, top=60, left=100');           
        }
        else
        {
                alert('Master not found for this entry! cant track');
        }
        //window.open (pageURL+, title, 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=500, height=300, top=60, left=100');
        
}

function addMawbFun(type,id)
{
        var mawbNum = $('#'+id+'mawbNum').val();
        
        var consoleNumber = $('#'+id+'consoleNumber').val();
        var customer = $('#'+id+'customer').val();
        //var etdDate = $('#'+id+'etdDate').val();
        //var etdTime = $('#'+id+'etdTime').val();
        var etaDate = $('#'+id+'etaDate').val();
        var etaTime = $('#'+id+'etaTime').val();
        //var ataDate = $('#'+id+'ataDate').val();
        //var ataTime = $('#'+id+'ataTime').val();
        var flightCode = $('#'+id+'flightCode').val();
        var flightNum = $('#'+id+'flightNum').val();
        var slac = $('#'+id+'slac').val();
        var pmcOrLoose = $('#'+id+'pmcOrLoose').val();
        var chgWeight = $('#'+id+'chgWeight').val();
        var remarksInClass = $('#'+id+'remarksInClass').val();
        var shipmentStatus = $('#'+id+'shipmentStatus').val();
        var trackSource = $('#'+id+'trackSource').val();
        var speakWith = $('#'+id+'speakWith').val();
        var oneFStatus = $('#'+id+'oneFStatus').val();
        var oneFStatusComment = $('#'+id+'oneFStatusComment').val();
        var station = $('#'+id+'station').val();
                        
        date_regex = /^(0[1-9]|1[012])[- . \/](0[1-9]|[12][0-9]|3[01])[- .\/]\d\d$/;
        time_regex = /^(0[0-9][0-5][0-9]|1[0-9][0-5][0-9]|2[0-3][0-5][0-9])$/;
        mawb_regex = /^(\d\d\d-\d\d\d\d\d\d\d\d|\d\d\d-\d\d\d\d\d\d\d\d([A-L]))$/;
        hawb_regex = /^([a-z]|[A-Z]|[0-9]|[-])*$/;
        pmc_regex = /^(Loose|\d\d|\d)$/;
        cust_regex = /^([a-z]|[A-Z]|[0-9]|[ ])*$/;
        
        if(trackSource== 'CALL')
        {
                if(speakWith=='')
                {
                        alert('S/W is a mandatory field!');
                        $('#processingStatus').html("<img src='/static/img/error.gif' />");
                        return false;
                }
        }
        
        //Mandatory fields
        if(mawbNum=='')
        {
                alert('Master # is a mandatory field!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        if(etaDate=='')
        {
                alert('ETA Date is a mandatory field!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        /*if(etaTime=='')
        {
                alert('ETA Time is a mandatory field!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        if(shipmentStatus=='')
        {
                alert('Shipment Status is a mandatory field!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        //Number fields
        if(isNaN(slac))
        {
                alert('SLAC(CTNs) should be a number!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        if(isNaN(consoleNumber))
        {
                alert('Consol # should be a number!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        if(isNaN(chgWeight))
        {
                alert('CHG. WGHT. should be a number!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        //Field specific rules
        if(mawbNum.search(mawb_regex) == -1)
        {               
                alert('Master # should consist of ddd-ddddddddC format. Here all "d" are digits & "C" is any capital character between A-F or nothing, eg. 123-23342312A or 123-12345678!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        if(consoleNumber != "" && consoleNumber.length != 6)
        {
                alert('Consol # must be 6 digits!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        if(flightCode != "" && flightCode.length != 2)
        {
                alert('Flight Code lenght must be 2!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        if(slac != "" && slac.length > 5)
        {
                alert('SLAC(CTNs) must be upto 5 digits!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }       
        
        if(chgWeight != "" && chgWeight.length > 5)
        {
                alert('CHG. WGHT. must be upto 5 digits!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        /*
        if(pmcOrLoose != 'Loose' && pmcOrLoose.search(pmc_regex) == -1)
        {
                alert('PMC/LOOSE must be Loose or of 2 digits!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        
        if(customer != "" && customer.search(cust_regex) == -1)
        {
                alert('Customer must contain only alpha-numeric characters!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        /*
        if(shipmentStatus == "COB")
        {
                if(recoveryNum == "" )
                        {
                                alert('Recovery# must contain value!!');
                                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                                return false;
                        }
                if(oneFStatus == "")
                {
                        alert('1F Status must contain value!!');
                        $('#processingStatus').html("<img src='/static/img/error.gif' />");
                        return false;
                }
        }
        */
        
        //Time fields
        /*
        if(ataTime.search(time_regex) == -1 && ataTime != "")
        {
                alert('ATA Time must have hhmm (0000-2359) format!!');
                return false;                   
        }
        if(etdTime.search(time_regex) == -1 && etdTime != "")
        {
                alert('ETD Time must have hhmm (0000-2359) format!!');
                return false;           
                        
        }
        if(etaTime.search(time_regex) == -1 && etaTime != "")
        {
                alert('ETA Time must have hhmm (0000-2359) format!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;   
                        
        }
        
        //Date fields
        
        /*if(etdDate.search(date_regex) == -1 && etdDate != "")
        {
                alert('ETD Date must have dd-mm-yyyy format!!');
                return false;
        }*/
        if(etaDate.search(date_regex) == -1 && etaDate != "")
        {
                alert('ETA Date must have mm-dd-yy format!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }
        
        /*if(ataDate.search(date_regex) == -1 && ataDate != "")
        {
                alert('ATA Date must have dd-mm-yyyy format!!');
                return false;
        }*/
        /*if(cobDate.search(date_regex) == -1 && cobDate != "")
        {
                alert('COB Date must have dd-mm-yyyy format!!');
                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                return false;
        }*/

        if(type=='update')
        {
                
                //ajaxWithSerialize('n','processingStatus','/process_it/mawbAction/',$('#formid_'+id).serialize()); //original update call
                
                var values = $('#formid_'+id).serialize()
                
                //ajaxWithSerialize('n','processingStatus','/process_it/mawbAction/','actionType=delete&'+values);
                
                //Calling url
                    $.ajax({
                        url: "/process_it/updateMawbEntry/",
                        type: "post",
                        data: values,
                        success: function(msg){
                                $("#"+id+"_update").attr("src","/static/img/save.gif");
                                $("#"+id+"lastUpdatedByUser").val(msg['name']);
                                $("#"+id+"lastUpdatedDate").val(msg['date']);
                                $("#"+id+"lastUpdatedTime").val(msg['time']);
                                $('#'+id+'mawbNum').css("background-color","#F7F2B2");
                                $("#"+id+"_row").css("background-color","#F7F2B2");
                                if(msg['cob'])
                                                {
                                                        $('#'+id+'_row').css('display','None');
                                                }
                        },
                        beforeSend: function() {                
                                $("#"+id+"_update").attr("src","/static/img/processing.gif");
                                 
                        }
                    });
                /*
                if(shipmentStatus == "COB")
                {
                        $('#'+id+'_row').css('display','None');
                }*/
                
        }
        
        if(type=='add')
        {
                var values = $('#mawb_entry_form').serialize(); 
                
                //ajaxWithSerialize('n','processingStatus','/process_it/mawbAction/','actionType=delete&'+values);
                
                //Calling url
                    $.ajax({
                        url: "/process_it/addMawbEntry/",
                        type: "post",
                        data: values,
                        success: function(msg){
                                
                     //           location.reload();      
                                $('#processingStatus').html("<img src='/static/img/done.gif' />");
                        },
                        beforeSend: function() {                
                                $("#processingStatus").html("<img src='/static/img/processing.gif' />");
                                 
                        },
                        error:function(){
                                $('#processingStatus').html("<img src='/static/img/error.gif' />");
                        }   
                    });
        }
}


function validateMawb()
{
        var values = $('#mawb_entry_form').serialize(); 
        alert(values);
        return;
        if($('#mawbNum').val() == "")
        {
                alert('please enter Master #!!');
                return false;
        }
        else
        {
                //Calling url
            $.ajax({
                url: "/process_it/validateMawbEntry/",
                type: "post",
                data: values,
                success: function(msg){
                        if(msg['exists'])
                                {
                                alert('master already exists');
                                }
                        else
                                {
                                addMawbFun('add','');                           

                                }
                }
            });
                
        }
        
}       

function filterMenu()
{
$(".topMenuAction").click( function() {
        if ($("#openCloseIdentifier").is(":hidden")) {                                  
                $("#topMenuImage").html("<img src='/static/img/close_it.png'/>");
                $("#openCloseIdentifier").show();
                $("#mail_list_div").css("height","67.6%");
        } else {                                        
                $("#topMenuImage").html("<img src='/static/img/alt.png'/>");
                $("#openCloseIdentifier").hide();
                $("#mail_list_div").css("height","94%");
        }
});  
}

function verticalMenu()
{
         document.getElementById('openCloseMenu')
                 
$(".rightMenuAction").hover( function() {
        if ($("#openCloseMenu").is(":hidden")) {
                $("#openMenuImage").html("<img src='/static/img/black.png' style='width: 10px; height:50px; ' />");
                $("#data_div_paprocess").css("width","88.8%");
                
                $("#openCloseMenu").show();
        } else {                                        
                $("#openMenuImage").html("<img src='/static/img/black.png' style='width: 10px; height:50px; ' />");
                $("#data_div_paprocess").css("width","100%");
                
                $("#openCloseMenu").hide();
        }
}); 

}

function clearMenu()
        {
        $('#date').val('');
        $('#from').val('');
        $('#subject').val('');
        $('#to').val('');
        $('#attach').attr('checked',false);
        $('#category').val('all');
        $('#mailbox').val('lax_import');
        $('#mailbox').val('DFW_MailBox');        
        $('#mail_filter_form').submit();
}

myMenu = null;

function popupMenu(e,mail_id){
  hideMyMenu();
  //if(!$('*')){
        if(!document.all){ 
        /*
        myMenu = $('#myMenu_'+mail_id);
        $('#'+myMenu).css('left',e.pageX+'px');
        $('#'+myMenu).css('top',e.pageY+'px');
        $('#'+myMenu).css('display','block');
        */
        myMenu = document.getElementById('myMenu_'+mail_id);
        
        myMenu.style.left = e.pageX+'px';
        
        
        if(e.pageY >= (window.innerHeight - 200))
                { myMenu.style.top  = (e.pageY-115)+'px'; }
        else
                { myMenu.style.top  = e.pageY+'px'; }
    myMenu.style.display = 'block';
        
  }
  else {        
        /*
        myMenu = $('#myMenu_'+mail_id);
        $('#'+myMenu).css('left',(e.clientX+$(document.body).scrollLeft())+'px');
        $('#'+myMenu).css('top',(e.clientY+$(document.body).scrollTop())+'px');
        $('#'+myMenu).css('display','block');
    */
        myMenu = document.getElementById('myMenu_'+mail_id);
    myMenu.style.left = (e.clientX+document.body.scrollLeft)+'px';
    if((e.clientY+document.body.scrollTop ) >= (window.innerHeight - 200))
                { myMenu.style.top  = ((e.clientY+document.body.scrollTop ) - 115)+'px'; }
        else
                { myMenu.style.top  = (e.clientY+document.body.scrollTop )+'px'; }
    myMenu.style.display = 'block';
        
  }
  return false;
}

function hideMyMenu(){
          if(myMenu){
            myMenu.style.display = 'none';
            myMenu = null;
          }
        }

myflagMenu = null;

function flag_popupMenu(e,mail_id){
  hide_myflagMenu();
  if(!document.all){    
        myflagMenu = $('#myMenu_'+mail_id);
        $('#'+myflagMenu).css('left',e.pageX+'px');
        $('#'+myflagMenu).css('top',e.pageY+'px');
        $('#'+myflagMenu).css('display','block');
        /*
        myflagMenu = document.getElementById('myMenu_'+mail_id);
    myflagMenu.style.left = e.pageX+'px';
    myflagMenu.style.top  = e.pageY+'px';
    myflagMenu.style.display = 'block';
        */
  }
  else {        
  
        myflagMenu = $('#myMenu_'+mail_id);
        $('#'+myflagMenu).css('left',(e.clientX+$(document.body).scrollLeft())+'px');
        $('#'+myflagMenu).css('top',(e.clientY+$(document.body).scrollTop())+'px');
        $('#'+myflagMenu).css('display','block');
        
    /*
    myflagMenu = document.getElementById('myMenu_'+mail_id);
    myflagMenu.style.left = (e.clientX+document.body.scrollLeft)+'px';
    myflagMenu.style.top  = (e.clientY+document.body.scrollTop )+'px';
    myflagMenu.style.display = 'block';
        */
  }
  return false;
}

function hide_myflagMenu(){
          if(myflagMenu){
          $('#'+myflagMenu).css('display','none');
            //myflagMenu.style.display = 'none';
            myflagMenu = null;
          }
        }
        
function show_task(e){

        $('#taskDiv').css('display','block');
        $('#taskDiv').css('left',e.pageX+'px');
        $('#taskDiv').css('top',e.pageY+'px');
        ajaxWithSerialize('n','taskDiv','/process_it/getTasks/','actionType=getTasks');
}

function hide_task(e){

        $('#taskDiv').css('display','None');
}
function chk_ajax(divId,url,val){       

       $.post(url,
               val,
               function(responseData) {
                 $('#'+divId).html(responseData);
               
               }
       );
}

function ajaxWithSerialize(refresh_flag,divID,url,val)
{       
        $.ajax({
                  type: "POST",
                  url: url,
                  data: val,
                  success: function(msg){
        
                          if(document.getElementById(divID))
                          {
                                  document.getElementById(divID).innerHTML=msg;
                          }
                          //document.getElementById("processing_status").innerHTML="";
                          if(refresh_flag=='y')
                        	  location.reload(true);
                          $.unblockUI();
                  },
              
                  beforeSend: function() {       
                	                $.blockUI({ message: '<br ><h1><img src="/static/img/ajax-loader2.gif" width="120" /></h1><br>' });
                	        }
                  
                });
}

function ajaxWithSerializeFlag(refresh_flag,divID,url,val){     

        $.ajax({
                  type: "POST",
                  url: url,
                  data: val,
                  success: function(msg){
                                
                           if($('#'+divID))
                                  {
                                          $('#'+divID).html(''+msg);
                                  }
                          
                          if(refresh_flag=='y')
                           location.reload();
                   
                  },
                  beforeSend: function() {
                  
                           if($('#'+divID))
                          {
                                  $('#'+divID).html("<img src='/static/img/processing.gif/'>");

                          }
                          },
                 complete: function() {
                                        ajaxWithSerialize('n','taskDiv','/process_it/getTasks/','actionType=getTasks');
                 }
                 
                });
}
function view_email(email_id)
{
        read = $('#readcount').html();
        unread = $('#unreadcount').html();
        if($('#selected_email_id').val()!=='')
        {
                $('#'+$('#selected_email_id').val()).css('background-color','#FFFFFF');
        }
        if($('#selected_email_id').val()!==email_id)
        {
                ajaxWithSerialize('n','mail_details','/process_it/getMailBody/','mail_id='+email_id);
                if ($('#read_'+email_id).attr('src') == "/static/img/unread.jpg")
                        {
                        $('#read_'+email_id).attr('src',"/static/img/read.jpg");
                        $('#readcount').html(parseInt(read)+1);
                        $('#unreadcount').html(parseInt(unread)-1);
                        }
                        
        }
        
        $('#'+email_id).css('background-color','#BAE2FC'); 
        $('#selected_email_id').val(email_id); 
         
}
function view_email_new(email_id)
{
        if($('#selected_email_id').val()!=='')
        {
                $('#'+$('#selected_email_id').val()).css('background-color','#FFFFFF');
        }
        if($('#selected_email_id').val()!==email_id)
        {
                chk_ajax('mail_details','/get_mail_body','mail_id='+email_id);
        }
        
        $('#'+email_id).css('background-color','#BAE2FC'); 
        $('#selected_email_id').val(email_id); 
        
}

function buildMailTo(address, subject, body) {
    var strMail = 'mailto:' + encodeURIComponent(address)
                   + '?subject=' + encodeURIComponent(subject)
                   + '&body=' + encodeURIComponent(body);
    return strMail;
}

function rawurlencode (str) {
        str = (str + '').toString(); 
    // Tilde should be allowed unescaped in future versions of PHP (as reflected below), but if you want to reflect current
    // PHP behavior, you would need to add ".replace(/~/g, '%7E');" to the following.
    return encodeURIComponent(str).replace(/!/g, '%21').replace(/'/g, '%27').replace(/\(/g, '%28').
    replace(/\)/g, '%29').replace(/\*/g, '%2A');
}
function findEmailAddresses(StrObj) {
        var separateEmailsBy = "; ";
        var email = "<none>"; // if no match, use this
        var emailsArray = StrObj.match(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/gi);
        if (emailsArray) {
                email = "";
                for (var i = 0; i < emailsArray.length; i++) {
                        if (i != 0) email += separateEmailsBy;
                        email += emailsArray[i];
                }
        }
        return email;
}
function send_mail(send_type)
{
        mail_id = $('#selected_email_id').val();
        to=findEmailAddresses($('#curr_email_to').html());
        from=findEmailAddresses($('#curr_email_from').html());
        subject=$('#curr_email_subject').html();
        cc=findEmailAddresses($('#curr_email_cc').html());
        body=$('#curr_email_body').html();
        var read = $('#readcount').html();
        var unread = $('#unreadcount').html();
        /*
        document.forms['mail_form']['body'].innerHTML = body;
        document.mail_form.action = link;
        document.mail_form.action = "mailto: Loretta.Atuatasi@Cevalogistics.com?cc=DL-AM-US-Boeingyyz@Cevalogistics.com&subject=Boeing";
        document.mail_form.submit();
        return;
        */
        //body1=String($('#mail_body2').val());//.substring(0,1250);
        //body1=$('#mail_body2').val().substring(0,prompt("number of character","")); 
        //$.copy(body1); 
   
        // alert(body1);
        //alert(body);
        //var strTest = buildMailTo('abc@xyz.com', 'Foo&foo', 'Bar\nBar');

        //window.open(strTest);
        if(from == null)
        {
                alert('No mail selected!');
                return false;
        }
        var link = "mailto:"+from             
                  + "?cc="+cc             
                  + "&subject=" + encodeURIComponent(subject)   ;
                 
//                              + "&body=" + encodeURIComponent(body);      
/*
        window = window.open(link, 'emailWindow');
        if (window && window.open && !window.closed)        
                  window.close();
*/
        //window.location='mailto:'+encodeURIComponent(to)+'?subject='+encodeURIComponent(subject)+'&cc='+encodeURIComponent(cc)+'&body='+$('#mail_body2').val();    
   
         //window.location="mailto:To:LAX Air Import <laximport@cevalogistics.com>, [SH]-AM-US-LAX Air Export" + email or attachments.";
        
    switch (send_type)
    {
    case "newMail":
                link = 'mailto:';
                window.location.href = link; 
      break;
    case "reply":
                if(mail_id=='')
                        {alert('No Mail selected');}
                else
                        {link = "mailto:"+from+"?cc="+cc+"&subject="+subject; window.location.href = link; }                          //+"&body="+body;
      break;
    case "replyAll":
                if(mail_id=='')
                        {alert('No Mail selected');}
                else
                        {link = 'mailto:'+from+';'+to+'?cc='+cc+'&subject='+subject; window.location.href = link; }
      break;
    case "forward":
                if(mail_id=='')
                        {alert('No Mail selected');}
                else
                        {link = "mailto:?subject="+subject; window.location.href = link; }
      break;
    case "1monthOld":
                if(mail_id=='')
                        alert('No Mail selected');
                else
                {
                        $('#'+mail_id).css('display','None');
                        $('#mail_details').html('');
                        ajaxWithSerialize('n','processingStatus','/process_it/mailAction/','actionType=1monthOld&mail_id='+mail_id);
                        $('#readcount').html(parseInt(read)-1);
                }
      break;
        case "unread":                              
                if(mail_id=='')
                        alert('No Mail selected');
                else
                {
                        if ($('#read_'+mail_id).attr('src') == "/static/img/unread.jpg")
                        {
                        $.ajax({ type: 'POST', 
                                         url: '/process_it/getMailBody/',
                                         data: 'mail_id='+mail_id+'&status=read', 
                                                
                                        });
                         $('#read_'+mail_id).attr('src',"/static/img/read.jpg");
                         $('#readcount').html(parseInt(read)+1);
                         $('#unreadcount').html(parseInt(unread)-1);
                        }
                else if($('#read_'+mail_id).attr('src') == "/static/img/read.jpg")
                        {
                        $.ajax({ type: 'POST',
                                         url: '/process_it/getMailBody/',
                                         data: 'mail_id='+mail_id+'&status=unread', 
                        
                                });
                        $('#read_'+mail_id).attr('src',"/static/img/unread.jpg");
                        $('#readcount').html(parseInt(read)-1);
                        $('#unreadcount').html(parseInt(unread)+1);
                        }
                }
      break;
    case "delete":                              
                if(mail_id=='')
                        alert('No Mail selected');
                else
                {
                        $('#'+mail_id).css('display','None');
                        $('#mail_details').html('');
                        ajaxWithSerialize('n','processingStatus','/process_it/mailAction/','actionType=delete&mail_id='+mail_id);
                        $('#readcount').html(parseInt(read)-1);
                }
      break;
    default:
                alert('invalid selection'); 
    }
   
}


function send_mawb(send_type)
{
        switch (send_type)
    {
            case "exporttoexcel":                              
                window.open('/process_it/exportExcel/','');
            break;
            case "prealerttoexcel":                              
                window.open('/process_it/preAlertExcel/','');
              break;
            case "export_excel_new":                              
                window.open('/process_it/export_excel_new/','');
              break;
            case "DFWexporttoexcel":                              
                window.open('/process_it/DFWexportExcel/','');
            break;
            case "performEvalutation":                              
                window.open('/process_it/performEvalutation/','');
            break;
            
            

            default:
                        alert('invalid selection'); 
    }
            
}

function refreshscreen()
{
        $.ajax({
        url: "/process_it/refreshScreen/",
        type: "post",        
        success: function(){                    
                        location.reload();
        }        
    });
}