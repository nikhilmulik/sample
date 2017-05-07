
var red = function(key, values) {
	var count_day0 = 0;
	var count_day1 = 0;
	var count_day2 = 0;
	var count_day3 = 0;
	var count_day4 = 0;
	var count_day5 = 0;
	var count_day6 = 0;
	var count_day7to10 = 0;
	var count_day11to15 = 0;
	var count_day16to30 = 0;
	var count_day30 = 0;
	var other_count = 0;
	var age_day0to2 = 0;
	var age_day3to7 = 0;
	var age_day8to30 = 0;
	var age_day30 = 0;
	var age_other_count = 0;
values.forEach(function(doc) {
	count_day0 += doc.unbilled_day0; 
	count_day1 += doc.unbilled_day1; 
	count_day2 += doc.unbilled_day2; 
	count_day3 += doc.unbilled_day3; 
	count_day4 += doc.unbilled_day4; 
	count_day5 += doc.unbilled_day5; 
	count_day6 += doc.unbilled_day6; 
	count_day7to10 += doc.unbilled_day7to10; 
	count_day11to15 += doc.unbilled_day11to15;
	count_day16to30 += doc.unbilled_day16to30;
	count_day30 += doc.unbilled_day30;
	other_count += doc.other;
	age_day0to2 += doc.pod_age0to2; 
	age_day3to7 += doc.pod_age3to7;
	age_day8to30 += doc.pod_age8to30;
	age_day30 += doc.pod_age30;
	age_other_count += doc.pod_ageOther;
});
return {
		unbilled_day0 : count_day0,
		unbilled_day1 : count_day1,
		unbilled_day2 : count_day2,
		unbilled_day3 : count_day3,
		unbilled_day4 : count_day4,
		unbilled_day5 : count_day5,
		unbilled_day6 : count_day6,
		unbilled_day7to10 : count_day7to10,
		unbilled_day11to15 : count_day11to15,
		unbilled_day16to30 : count_day16to30,
		unbilled_day30 : count_day30,
		other:other_count,
		pod_age0to2 : age_day0to2,
		pod_age3to7 : age_day3to7,
		pod_age8to30 : age_day8to30,
		pod_age30 : age_day30,
		pod_ageOther:age_other_count
		};
};

var final = function(key,value) {
    total_vol = value.unbilled_day0 + value.unbilled_day1 + value.unbilled_day2 + value.unbilled_day3 + value.unbilled_day4 + value.unbilled_day5 + value.unbilled_day6 + value.unbilled_day7to10 + value.unbilled_day11to15 + value.unbilled_day16to30 + value.unbilled_day30;
	
	total_age_vol = value.pod_age0to2 + value.pod_age3to7 + value.pod_age8to30 + value.pod_age30;
	if(total_vol > 0)
	{
		unbilled_day0_p = value.unbilled_day0 * 100 / total_vol; 
		unbilled_day1_p = value.unbilled_day1 * 100 / total_vol; 
		unbilled_day2_p = value.unbilled_day2 * 100 / total_vol; 
		unbilled_day3_p = value.unbilled_day3 * 100 / total_vol; 
		unbilled_day4_p = value.unbilled_day4 * 100 / total_vol; 
		unbilled_day5_p = value.unbilled_day5 * 100 / total_vol; 
		unbilled_day6_p = value.unbilled_day6 * 100 / total_vol; 
		unbilled_day7to10_p = value.unbilled_day7to10 * 100 / total_vol;
		unbilled_day11to15_p = value.unbilled_day11to15 * 100 / total_vol;
		unbilled_day16to30_p = value.unbilled_day16to30 * 100 / total_vol;
		unbilled_day30_p = value.unbilled_day30 * 100 / total_vol;
		other_p = value.other * 100 / total_vol;
	}
	if(total_age_vol > 0)
	{
		pod_age0to2_p = value.pod_age0to2 * 100 / total_age_vol;
		pod_age3to7_p = value.pod_age3to7 * 100 / total_age_vol;
		pod_age8to30_p = value.pod_age8to30 * 100 / total_age_vol;
		pod_age30_p = value.pod_age30 * 100 / total_age_vol;
		pod_ageOther_p = value.pod_ageOther * 100 / total_age_vol;
	}
return { unbilled_day0 : value.unbilled_day0,
		 unbilled_day1 : value.unbilled_day1,
		 unbilled_day2 : value.unbilled_day2,
		 unbilled_day3 : value.unbilled_day3,
		 unbilled_day4 : value.unbilled_day4,
		 unbilled_day5 : value.unbilled_day5,
		 unbilled_day6 : value.unbilled_day6,
		 unbilled_day7to10 : value.unbilled_day7to10,
		 unbilled_day11to15 : value.unbilled_day11to15,
		 unbilled_day16to30 : value.unbilled_day16to30,
		 unbilled_day30 : value.unbilled_day30,
		 other : value.other,
		 pod_age0to2 : value.pod_age0to2,
		 pod_age3to7 : value.pod_age3to7,
		 pod_age8to30 : value.pod_age8to30,
		 pod_age30 : value.pod_age30,
		 pod_ageOther : value.pod_ageOther,
		 unbilled_day0_per : unbilled_day0_p,
		 unbilled_day1_per : unbilled_day1_p,
		 unbilled_day2_per : unbilled_day2_p,
		 unbilled_day3_per : unbilled_day3_p,
		 unbilled_day4_per : unbilled_day4_p,
		 unbilled_day5_per : unbilled_day5_p,
		 unbilled_day6_per : unbilled_day6_p,
		 unbilled_day7to10_per : unbilled_day7to10_p,
		 unbilled_day11to15_per : unbilled_day11to15_p,
		 unbilled_day16to30_per : unbilled_day16to30_p,
		 unbilled_day30_per : unbilled_day30_p,
		 unbilled_other_per : other_p,
		 pod_age0to2_per : pod_age0to2_p,
		 pod_age3to7_per : pod_age3to7_p,
		 pod_age8to30_per : pod_age8to30_p,
		 pod_age30_per : pod_age30_p,
		 pod_ageOther_per : pod_ageOther_p		 };
  };

var map_acc = function(){	
		
	var d0_unbilled = 0;
	var d1_unbilled = 0;
	var d2_unbilled = 0;
	var d3_unbilled = 0;
	var d4_unbilled = 0;
	var d5_unbilled = 0;
	var d6_unbilled = 0;
	var d7to10_unbilled = 0;
	var d11to15_unbilled = 0;
	var d16to30_unbilled = 0;
	var d30_unbilled = 0;
	var age0to2 = 0;
	var age3to7 = 0;
	var age8to30 = 0;
	var age30 = 0;
	var ageOther = 0;
	var pod_diff = 0;
	var date_diff = 0;
	var other = 0;
	var date,month,year = 0;
	date = this.extr_date.getDate();
	month = this.extr_date.getMonth() + 1;
	year = this.extr_date.getFullYear();
	
		date_diff = this.extr_date - this.pod_date;
		pod_diff = this.pod_entered_date - this.pod_date;
		date_diff = date_diff / (1000*60*60*24);
		pod_diff = pod_diff / (1000*60*60*24);
		
		if(pod_diff >= 0 & pod_diff <=2)
			age0to2 = 1;
		else if(pod_diff > 2 & pod_diff <= 7)
			age3to7 = 1;
		else if(pod_diff > 7 & pod_diff <= 30)
			age8to30 = 1;
		else if(pod_diff > 30)
			age30 = 1;
		else
			ageOther = 1;
		
		if(date_diff >= 0 & date_diff <1)
			d0_unbilled = 1;
		else if(date_diff >= 1 & date_diff <2)
			d1_unbilled = 1;
		else if(date_diff >= 2 & date_diff <3)
			d2_unbilled = 1;
		else if(date_diff >= 3 & date_diff <4)
			d3_unbilled = 1;
		else if(date_diff >= 4 & date_diff <5)
			d4_unbilled = 1;
		else if(date_diff >= 5 & date_diff <6)
			d5_unbilled = 1;
		else if(date_diff >= 6 & date_diff <7)
			d6_unbilled = 1;
		else if(date_diff >= 7 & date_diff <=10)
			d7to10_unbilled = 1;
		else if(date_diff > 10 & date_diff <=15)
			d11to15_unbilled = 1;
		else if(date_diff > 15 & date_diff <=30)
			d16to30_unbilled = 1;
		else if(date_diff > 30 )
			d30_unbilled = 1;
		else	
			other = 1;
			
		if(this.region === 'nsc' || this.region === 'corporate' || this.region === 'CORPORATE' || this.region === 'NSC')
		{
			emit({country:"US",region:'NSC',station:this.station,client:this.client,acc_code:this.acc_code, year:year, month:month, day:date}, 
			{
				unbilled_day0 : d0_unbilled,
				unbilled_day1 : d1_unbilled,
				unbilled_day2 : d2_unbilled,
				unbilled_day3 : d3_unbilled,
				unbilled_day4 : d4_unbilled,
				unbilled_day5 : d5_unbilled,
				unbilled_day6 : d6_unbilled,
				unbilled_day7to10 : d7to10_unbilled,
				unbilled_day11to15 : d11to15_unbilled,
				unbilled_day16to30 : d16to30_unbilled,
				unbilled_day30 : d30_unbilled,
				other:other,
				pod_age0to2 : age0to2,
				pod_age3to7 : age3to7,
				pod_age8to30 : age8to30,
				pod_age30 : age30,
				pod_ageOther : ageOther
			});
		}
		else
		{
		emit({country:"US",region:this.region,station:this.station,client:this.client,acc_code:this.acc_code, year:year, month:month, day:date},
			{
				unbilled_day0 : d0_unbilled,
				unbilled_day1 : d1_unbilled,
				unbilled_day2 : d2_unbilled,
				unbilled_day3 : d3_unbilled,
				unbilled_day4 : d4_unbilled,
				unbilled_day5 : d5_unbilled,
				unbilled_day6 : d6_unbilled,
				unbilled_day7to10 : d7to10_unbilled,
				unbilled_day11to15 : d11to15_unbilled,
				unbilled_day16to30 : d16to30_unbilled,
				unbilled_day30 : d30_unbilled,
				other:other,
				pod_age0to2 : age0to2,
				pod_age3to7 : age3to7,
				pod_age8to30 : age8to30,
				pod_age30 : age30,
				pod_ageOther : ageOther
			});
		}
		
};
  
var map1 = function(){	
		
	emit({country:this._id.country, region:this._id.region,station:this._id.station,client:this._id.client, year:this._id.year, month:this._id.month, day:this._id.day}, {
	unbilled_day0 : this.value.unbilled_day0 ,
	unbilled_day1 : this.value.unbilled_day1 ,
	unbilled_day2 : this.value.unbilled_day2 ,
	unbilled_day3 : this.value.unbilled_day3 ,
	unbilled_day4 : this.value.unbilled_day4 ,
	unbilled_day5 : this.value.unbilled_day5 ,
	unbilled_day6 : this.value.unbilled_day6 ,
	unbilled_day7to10 : this.value.unbilled_day7to10 ,
	unbilled_day11to15 : this.value.unbilled_day11to15,
	unbilled_day16to30 : this.value.unbilled_day16to30,
	unbilled_day30 : this.value.unbilled_day30 ,
	other:this.value.other,
	pod_age0to2 : this.value.pod_age0to2,
	pod_age3to7 : this.value.pod_age3to7,
	pod_age8to30 : this.value.pod_age8to30,
	pod_age30 : this.value.pod_age30,
	pod_ageOther : this.value.pod_ageOther
	});	
};

var map2 = function(){	
	
	emit({country:this._id.country, region:this._id.region,station:this._id.station, year:this._id.year, month:this._id.month, day:this._id.day}, {		unbilled_day0 : this.value.unbilled_day0 ,
	unbilled_day1 : this.value.unbilled_day1 ,
	unbilled_day2 : this.value.unbilled_day2 ,
	unbilled_day3 : this.value.unbilled_day3 ,
	unbilled_day4 : this.value.unbilled_day4 ,
	unbilled_day5 : this.value.unbilled_day5 ,
	unbilled_day6 : this.value.unbilled_day6 ,
	unbilled_day7to10 : this.value.unbilled_day7to10 ,
	unbilled_day11to15 : this.value.unbilled_day11to15,
	unbilled_day16to30 : this.value.unbilled_day16to30,
	unbilled_day30 : this.value.unbilled_day30 ,
	other:this.value.other,
	pod_age0to2 : this.value.pod_age0to2,
	pod_age3to7 : this.value.pod_age3to7,
	pod_age8to30 : this.value.pod_age8to30,
	pod_age30 : this.value.pod_age30,
	pod_ageOther : this.value.pod_ageOther
	});	
};

var map3 = function(){	
	
	emit({country:this._id.country, region:this._id.region, year:this._id.year, month:this._id.month, day:this._id.day}, {unbilled_day0 : this.value.unbilled_day0 ,
	unbilled_day1 : this.value.unbilled_day1 ,
	unbilled_day2 : this.value.unbilled_day2 ,
	unbilled_day3 : this.value.unbilled_day3 ,
	unbilled_day4 : this.value.unbilled_day4 ,
	unbilled_day5 : this.value.unbilled_day5 ,
	unbilled_day6 : this.value.unbilled_day6 ,
	unbilled_day7to10 : this.value.unbilled_day7to10 ,
	unbilled_day11to15 : this.value.unbilled_day11to15,
	unbilled_day16to30 : this.value.unbilled_day16to30,
	unbilled_day30 : this.value.unbilled_day30 ,
	other:this.value.other,
	pod_age0to2 : this.value.pod_age0to2,
	pod_age3to7 : this.value.pod_age3to7,
	pod_age8to30 : this.value.pod_age8to30,
	pod_age30 : this.value.pod_age30,
	pod_ageOther : this.value.pod_ageOther
	});	
};

var map4 = function(){	
			
	emit({country:this._id.country, year:this._id.year, month:this._id.month, day:this._id.day}, {unbilled_day0 : this.value.unbilled_day0 ,
	unbilled_day1 : this.value.unbilled_day1 ,
	unbilled_day2 : this.value.unbilled_day2 ,
	unbilled_day3 : this.value.unbilled_day3 ,
	unbilled_day4 : this.value.unbilled_day4 ,
	unbilled_day5 : this.value.unbilled_day5 ,
	unbilled_day6 : this.value.unbilled_day6 ,
	unbilled_day7to10 : this.value.unbilled_day7to10 ,
	unbilled_day11to15 : this.value.unbilled_day11to15,
	unbilled_day16to30 : this.value.unbilled_day16to30,
	unbilled_day30 : this.value.unbilled_day30 ,
	other:this.value.other,
	pod_age0to2 : this.value.pod_age0to2,
	pod_age3to7 : this.value.pod_age3to7,
	pod_age8to30 : this.value.pod_age8to30,
	pod_age30 : this.value.pod_age30,
	pod_ageOther : this.value.pod_ageOther
	});
};

//var res = db.hawb_copy.mapReduce(map, red, {query : { inv_date : {$gte:curDateTime1,$lte:curDateTime2}},finalize : final, out : { "merge" : "hawb_summary_station_month" , "db" : "domestic"}}); // query : { inv_date : {$gte:curDateTime1,$lte:curDateTime2}},

var curDateTime1 = new Date();
curDateTime1.setDate(curDateTime1.getDate() - 4);


var res_acc = db.src_dom_unbilled.mapReduce(map_acc, red, {query : { extr_date : {$gte:curDateTime1}},finalize : final, out :{ "merge" : "view_dom_unbilled_summary_acc_code_with_pod_age" }});
var res1 = db.view_dom_unbilled_summary_acc_code_with_pod_age.mapReduce(map1, red, {finalize : final, out :{ "merge" : "view_dom_unbilled_summary_client_with_pod_age" }});
var res2 = db.view_dom_unbilled_summary_client_with_pod_age.mapReduce(map2, red, {finalize : final, out :{ "merge" : "view_dom_unbilled_summary_station_with_pod_age" }});
var res3 = db.view_dom_unbilled_summary_station_with_pod_age.mapReduce(map3, red, {finalize : final, out :{ "merge" : "view_dom_unbilled_summary_region_with_pod_age" }});
var res4 = db.view_dom_unbilled_summary_region_with_pod_age.mapReduce(map4, red, {finalize : final, out :{ "merge" : "view_dom_unbilled_summary_country_with_pod_age" }});
