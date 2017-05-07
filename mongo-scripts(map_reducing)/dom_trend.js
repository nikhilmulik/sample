var map = function(){

    var podToinv = 0;
    var shipToinv = 0;
    var corrected = 0;
	var billed_after_ship = 0;
	var billed_after_pod = 0;
	
	if(this.inv_date > this.ship_date) shipToinv = this.inv_date - this.ship_date;
	
	if(this.inv_date > this.pod_date) podToinv = this.inv_date - this.pod_date;
	
	if((this.inv_date > this.ship_date) && (this.inv_date < this.pod_date)) 
	{
		billed_after_ship = 1;
	}
	else if((this.inv_date > this.pod_date))
    {
		billed_after_pod = 1;
	}
    podToinv = podToinv / (1000*60*60*24);
	shipToinv = shipToinv / (1000*60*60*24);
	if(this.corrected_flag === 'Y')
        corrected = 1;

    var d1_billed_after_ship, d2_billed_after_ship, d3_billed_after_ship, d4_billed_after_ship =0;
	var d1_billed_after_pod, d2_billed_after_pod, d3_billed_after_pod, d4_billed_after_pod =0;

    if(billed_after_ship === 1)
    {	
	    if(shipToinv>0 & shipToinv<=1)
			d1_billed_after_ship =1;

		if(shipToinv>1 & shipToinv<=2)
			d2_billed_after_ship =1;

		if(shipToinv>2 & shipToinv<=3)
			d3_billed_after_ship =1;

		if(shipToinv>3)
			d4_billed_after_ship =1;
	}		
	if(billed_after_pod === 1)
    {	
	    if(podToinv>0 & podToinv<=1)
			d1_billed_after_pod =1;

		if(podToinv>1 & podToinv<=2)
			d2_billed_after_pod =1;

		if(podToinv>2 & podToinv<=3)
			d3_billed_after_pod =1;

		if(podToinv>3)
			d4_billed_after_pod =1;
	}
if(this.metadata.report_type === "volume") 
{	
	if(this.metadata.region === 'nsc' || this.metadata.region === 'corporate' || this.metadata.region === 'NSC' || this.metadata.region === 'CORPORATE')
	{
		emit({country:this.metadata.country ,region:'nsc', station:this.metadata.station, client:this.client, year:this.metadata.year, month:this.metadata.month},
			{volume:1,
			 pod_inv:podToinv,
			 ship_inv:shipToinv,
			 corrected_count:0,
			 billed_after_ship_day1:d1_billed_after_ship,
			 billed_after_ship_day2:d2_billed_after_ship,
			 billed_after_ship_day3:d3_billed_after_ship,
			 billed_after_ship_day4:d4_billed_after_ship,
			 billed_after_pod_day1:d1_billed_after_pod,
			 billed_after_pod_day2:d2_billed_after_pod,
			 billed_after_pod_day3:d3_billed_after_pod,
			 billed_after_pod_day4:d4_billed_after_pod,
			 volume_billed_after_ship : billed_after_ship,
			 volume_billed_after_pod : billed_after_pod });
	}
	else
	{
		emit({country:this.metadata.country ,region:this.metadata.region, station:this.metadata.station, client:this.client, year:this.metadata.year, month:this.metadata.month},
		{volume:1,
    	 pod_inv:podToinv,
		 ship_inv:shipToinv,
		 corrected_count:0,
		 billed_after_ship_day1:d1_billed_after_ship,
		 billed_after_ship_day2:d2_billed_after_ship,
		 billed_after_ship_day3:d3_billed_after_ship,
		 billed_after_ship_day4:d4_billed_after_ship,
		 billed_after_pod_day1:d1_billed_after_pod,
		 billed_after_pod_day2:d2_billed_after_pod,
		 billed_after_pod_day3:d3_billed_after_pod,
		 billed_after_pod_day4:d4_billed_after_pod,
		 volume_billed_after_ship : billed_after_ship,
		 volume_billed_after_pod : billed_after_pod });
	}
}
else if(this.metadata.report_type === "adjustment") 
{

if(this.metadata.region === 'nsc' || this.metadata.region === 'corporate' || this.metadata.region === 'NSC' || this.metadata.region === 'CORPORATE')
	{
		emit({country:this.metadata.country ,region:'nsc', station:this.metadata.station, client:this.client, year:this.metadata.year, month:this.metadata.month},
			{volume:0,
			 pod_inv:0,
			 ship_inv:0,
			 corrected_count:1,
			 billed_after_ship_day1:0,
			 billed_after_ship_day2:0,
			 billed_after_ship_day3:0,
			 billed_after_ship_day4:0,
			 billed_after_pod_day1:0,
			 billed_after_pod_day2:0,
			 billed_after_pod_day3:0,
			 billed_after_pod_day4:0,
			 volume_billed_after_ship : 0,
			 volume_billed_after_pod : 0 });
	}
	else
	{
		emit({country:this.metadata.country ,region:this.metadata.region, station:this.metadata.station, client:this.client, year:this.metadata.year, month:this.metadata.month},
		{volume:0,
    	 pod_inv:0,
		 ship_inv:0,
		 corrected_count:1,
		 billed_after_ship_day1:0,
		 billed_after_ship_day2:0,
		 billed_after_ship_day3:0,
		 billed_after_ship_day4:0,
		 billed_after_pod_day1:0,
		 billed_after_pod_day2:0,
		 billed_after_pod_day3:0,
		 billed_after_pod_day4:0,
		 volume_billed_after_ship : 0,
		 volume_billed_after_pod : 0 });
	}

}

};

var red = function(key, values) {
    var s_v = 0;
	var s_pi = 0;
	var s_si = 0;
	var s_corr = 0;
	var s_d1_billed_after_ship = 0;
	var s_d2_billed_after_ship = 0;
	var s_d3_billed_after_ship = 0;
	var s_d4_billed_after_ship = 0;
	var s_d1_billed_after_pod = 0;
	var s_d2_billed_after_pod = 0;
	var s_d3_billed_after_pod = 0;
	var s_d4_billed_after_pod = 0;
	var s_v_aft_pod = 0;
	var s_v_aft_ship = 0;
   
    values.forEach(function(doc) {
	
	s_v_aft_pod += doc.volume_billed_after_pod;
	
	s_v_aft_ship += doc.volume_billed_after_ship;
	
	s_v += doc.volume;

	s_pi += doc.pod_inv;

	s_si += doc.ship_inv;
	
	s_corr += doc.corrected_count;

	s_d1_billed_after_ship += doc.billed_after_ship_day1;

	s_d2_billed_after_ship += doc.billed_after_ship_day2;

	s_d3_billed_after_ship += doc.billed_after_ship_day3;

	s_d4_billed_after_ship += doc.billed_after_ship_day4;
	
	s_d1_billed_after_pod += doc.billed_after_pod_day1;

	s_d2_billed_after_pod += doc.billed_after_pod_day2;

	s_d3_billed_after_pod += doc.billed_after_pod_day3;

	s_d4_billed_after_pod += doc.billed_after_pod_day4;
	
    });

return { volume:s_v,
         pod_inv:s_pi,
		 ship_inv:s_si,
		 corrected_count:s_corr,
		 billed_after_ship_day1:s_d1_billed_after_ship,
		 billed_after_ship_day2:s_d2_billed_after_ship,
		 billed_after_ship_day3:s_d3_billed_after_ship,
		 billed_after_ship_day4:s_d4_billed_after_ship,
		 billed_after_pod_day1:s_d1_billed_after_pod,
		 billed_after_pod_day2:s_d2_billed_after_pod,
		 billed_after_pod_day3:s_d3_billed_after_pod,
		 billed_after_pod_day4:s_d4_billed_after_pod,
		 volume_billed_after_ship:s_v_aft_ship,
		 volume_billed_after_pod:s_v_aft_pod };
  };

var final = function(key,value) {
    
	d = 31; //days in a month
	
	volume_a = value.volume/d;
	ship_inv_a = value.ship_inv/value.volume;
	pod_inv_a = value.pod_inv/value.volume;
    if(value.volume === 0)
		corrected_p = NaN
	else
		corrected_p = (value.corrected_count*100)/(value.volume);
	
    if(value.volume_billed_after_ship > 0){ 
		
		billed_after_ship_day1_p = (value.billed_after_ship_day1*100)/value.volume_billed_after_ship;

		billed_after_ship_day2_p = (value.billed_after_ship_day2*100)/value.volume_billed_after_ship;

		billed_after_ship_day3_p = (value.billed_after_ship_day3*100)/value.volume_billed_after_ship;

		billed_after_ship_day4_p = (value.billed_after_ship_day4*100)/value.volume_billed_after_ship;
	}
	else {
		
		billed_after_ship_day1_p=0;
		billed_after_ship_day2_p=0;
		billed_after_ship_day3_p=0;
		billed_after_ship_day4_p=0;
	}
	
	if(value.volume_billed_after_pod > 0){ 	
		
		billed_after_pod_day1_p = (value.billed_after_pod_day1*100)/value.volume_billed_after_pod;

		billed_after_pod_day2_p = (value.billed_after_pod_day2*100)/value.volume_billed_after_pod;

		billed_after_pod_day3_p = (value.billed_after_pod_day3*100)/value.volume_billed_after_pod;

		billed_after_pod_day4_p = (value.billed_after_pod_day4*100)/value.volume_billed_after_pod;
	}
	else{
		
		billed_after_pod_day1_p = 0;
		billed_after_pod_day2_p = 0;
		billed_after_pod_day3_p = 0;
		billed_after_pod_day4_p = 0;
	}
	
	volume_billed_after_pod_p = (value.volume_billed_after_pod*100)/value.volume;
	
	volume_billed_after_ship_p = (value.volume_billed_after_ship*100)/value.volume;
	
return { volume:value.volume,
         pod_inv:value.pod_inv,
		 ship_inv:value.ship_inv,
		 corrected_count:value.corrected_count,
		 billed_after_ship_day1:value.billed_after_ship_day1,
		 billed_after_ship_day2:value.billed_after_ship_day2,
		 billed_after_ship_day3:value.billed_after_ship_day3,
		 billed_after_ship_day4:value.billed_after_ship_day4,
		 billed_after_pod_day1:value.billed_after_pod_day1,
		 billed_after_pod_day2:value.billed_after_pod_day2,
		 billed_after_pod_day3:value.billed_after_pod_day3,
		 billed_after_pod_day4:value.billed_after_pod_day4,
		 volume_billed_after_ship:value.volume_billed_after_ship,
		 volume_billed_after_pod:value.volume_billed_after_pod,
		 volume_avg:volume_a,
		 pod_inv_avg:pod_inv_a,
		 ship_inv_avg:ship_inv_a,
		 corrected_per:100 - corrected_p,
		 billed_after_ship_day1_per:billed_after_ship_day1_p,
		 billed_after_ship_day2_per:billed_after_ship_day2_p,
		 billed_after_ship_day3_per:billed_after_ship_day3_p,
		 billed_after_ship_day4_per:billed_after_ship_day4_p,
		 billed_after_pod_day1_per:billed_after_pod_day1_p,
		 billed_after_pod_day2_per:billed_after_pod_day2_p,
		 billed_after_pod_day3_per:billed_after_pod_day3_p,
		 billed_after_pod_day4_per:billed_after_pod_day4_p,
         volume_billed_after_pod_per:volume_billed_after_pod_p,
		 volume_billed_after_ship_per:volume_billed_after_ship_p	};
  };

var map1 = function(){
 emit({country:this._id.country ,region:this._id.region, station:this._id.station, client:this._id.client, year:this._id.year, month:this._id.month},
		{volume:this.value.volume,
    	 pod_inv:this.value.pod_inv,
		 ship_inv:this.value.ship_inv,
		 corrected_count:this.value.corrected_count,
		 billed_after_ship_day1:this.value.billed_after_ship_day1,
		 billed_after_ship_day2:this.value.billed_after_ship_day2,
		 billed_after_ship_day3:this.value.billed_after_ship_day3,
		 billed_after_ship_day4:this.value.billed_after_ship_day4,
		 billed_after_pod_day1:this.value.billed_after_pod_day1,
		 billed_after_pod_day2:this.value.billed_after_pod_day2,
		 billed_after_pod_day3:this.value.billed_after_pod_day3,
		 billed_after_pod_day4:this.value.billed_after_pod_day4,
		 volume_billed_after_ship : this.value.volume_billed_after_ship,
		 volume_billed_after_pod : this.value.volume_billed_after_pod });
};

var map2 = function(){
 emit({country:this._id.country ,region:this._id.region, station:this._id.station, year:this._id.year, month:this._id.month},
		{volume:this.value.volume,
    	 pod_inv:this.value.pod_inv,
		 ship_inv:this.value.ship_inv,
		 corrected_count:this.value.corrected_count,
		 billed_after_ship_day1:this.value.billed_after_ship_day1,
		 billed_after_ship_day2:this.value.billed_after_ship_day2,
		 billed_after_ship_day3:this.value.billed_after_ship_day3,
		 billed_after_ship_day4:this.value.billed_after_ship_day4,
		 billed_after_pod_day1:this.value.billed_after_pod_day1,
		 billed_after_pod_day2:this.value.billed_after_pod_day2,
		 billed_after_pod_day3:this.value.billed_after_pod_day3,
		 billed_after_pod_day4:this.value.billed_after_pod_day4,
		 volume_billed_after_ship : this.value.volume_billed_after_ship,
		 volume_billed_after_pod : this.value.volume_billed_after_pod });
};

var map3 = function(){
 emit({country:this._id.country ,region:this._id.region, year:this._id.year, month:this._id.month},
		{volume:this.value.volume,
    	 pod_inv:this.value.pod_inv,
		 ship_inv:this.value.ship_inv,
		 corrected_count:this.value.corrected_count,
		 billed_after_ship_day1:this.value.billed_after_ship_day1,
		 billed_after_ship_day2:this.value.billed_after_ship_day2,
		 billed_after_ship_day3:this.value.billed_after_ship_day3,
		 billed_after_ship_day4:this.value.billed_after_ship_day4,
		 billed_after_pod_day1:this.value.billed_after_pod_day1,
		 billed_after_pod_day2:this.value.billed_after_pod_day2,
		 billed_after_pod_day3:this.value.billed_after_pod_day3,
		 billed_after_pod_day4:this.value.billed_after_pod_day4,
		 volume_billed_after_ship : this.value.volume_billed_after_ship,
		 volume_billed_after_pod : this.value.volume_billed_after_pod });
};  
  
var map4 = function(){
 emit({country:this._id.country, year:this._id.year, month:this._id.month},
		{volume:this.value.volume,
    	 pod_inv:this.value.pod_inv,
		 ship_inv:this.value.ship_inv,
		 corrected_count:this.value.corrected_count,
		 billed_after_ship_day1:this.value.billed_after_ship_day1,
		 billed_after_ship_day2:this.value.billed_after_ship_day2,
		 billed_after_ship_day3:this.value.billed_after_ship_day3,
		 billed_after_ship_day4:this.value.billed_after_ship_day4,
		 billed_after_pod_day1:this.value.billed_after_pod_day1,
		 billed_after_pod_day2:this.value.billed_after_pod_day2,
		 billed_after_pod_day3:this.value.billed_after_pod_day3,
		 billed_after_pod_day4:this.value.billed_after_pod_day4,
		 volume_billed_after_ship : this.value.volume_billed_after_ship,
		 volume_billed_after_pod : this.value.volume_billed_after_pod });
}; 


var curDateTime1 = new Date();
curDateTime1.setDate(curDateTime1.getDate() - 4);

var res = db.src_domestic_trend_vol_accuracy.mapReduce(map, red, {query : { "metadata.insert_date" : {$gte:curDateTime1}},finalize : final, out : { "merge" : "view_dom_trend_summary_acc_code" }});
var res1 = db.view_dom_trend_summary_acc_code.mapReduce(map1, red, {finalize : final, out : { "merge" : "view_dom_trend_summary_client" }});
var res2 = db.view_dom_trend_summary_client.mapReduce(map2, red, {finalize : final, out : { "merge" : "view_dom_trend_summary_station" }});
var res3 = db.view_dom_trend_summary_station.mapReduce(map3, red, {finalize : final, out : { "merge" : "view_dom_trend_summary_region" }});
var res4 = db.view_dom_trend_summary_region.mapReduce(map4, red, {finalize : final, out : { "merge" : "view_dom_trend_summary_country" }});
