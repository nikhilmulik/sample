
var map = function(){	
	var corr_vol = 0;
	var corr_vol_bb = 0;
	var corr_vol_imp = 0;
	var len = 0;
	var substr = 0;
	var str = 0;
	var accu_vol = 0;
	var log_vol = 0;
	var mawb_cnt = 0;
	var hawb_cnt = 0;
	var accur = {};
	var size_of_accuracy = 0;
	var suffix_flag = '';
	var temp_str = '';
	var corr_fin = 0;
	var corr_non_fin = 0;
	var inv_for_corr ='';
	
	if(this.division_code === 'AI' | this.division_code === 'OI')
	{
		if (this.file_type === 'BB_Log_Open')
		{	
			log_vol = 1;
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:0,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
		}
		if (this.file_type === 'BB_Inv_Reg')
		{	
			accu_vol = 1;
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:0,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
		}
		if (this.file_type === 'BB_Inv_Acc' )
		{
			accur = this.accuracy;
			for (key in accur)
			{
				if (accur.hasOwnProperty(key)) size_of_accuracy++;
			}

			if(size_of_accuracy > 0)
			{
				for(var i = 1; i <= size_of_accuracy; i++)
				{
					temp_str = "Accuracy" + i;
					if(accur[temp_str]["file_number_suffix"] != "")
					{
						suffix_flag = "true";
					}
					
				}
			}	
			corr_vol_bb = 1;
			if(suffix_flag != "")
			{
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:0,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
			}
		}
		if (this.file_type === 'BB_TONNAGE')
		{
			if(this.file_num)
			{
				mawb_cnt = 1;
			}
			hawb_cnt = this.hawb_cnt;
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:0,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
		}
	}
	
	else if(this.division_code === 'CA' | this.division_code === 'CO')
	{
		if (this.file_type === 'BB_Log_Open')
		{	
			log_vol = 1;
			if(this.station != "PDX")
			{
				if(this.invoice_num != "999999999999" & this.invoice_num != "888888888888" & this.importer != "DO NOT USE THIS ACCOUNT FOR ANY" & this.entry_num.indexOf("004       0 0") === -1 & this.entry_num.indexOf("          0 0") === -1 & this.entry_num.indexOf("000       0 0") === -1)
				{
				emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:corr_vol,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});	
				}
			}
			else
			{
				if(this.importer != "DO NOT USE THIS ACCOUNT FOR ANY" & this.entry_num.indexOf("004       0 0") === -1 & this.entry_num.indexOf("          0 0") === -1 & this.entry_num.indexOf("000       0 0") === -1)
				{
				emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:corr_vol,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});	
				}
			}
		}
		if (this.file_type === 'BB_Inv_Reg')
		{	
			re_string = /^[A-Z]{3}[0-9a-zA-Z]{7}[0]{2}$/;
			accu_vol = 1;
			if (re_string.test(this.invoice_num))
			{
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:corr_vol,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
			}
		}
		if (this.file_type === 'BB_Inv_Acc')
		{
			corr_vol_imp = 1;
			//this.invoice_num.substring(0,10)
			re_string = /^[A-Z]{3}[0-9a-zA-Z]{7}[0-9]{2}$/;
			
			if (re_string.test(this.invoice_num))
			{   
				if(this.accuracy.Accuracy1.reason_code.substring(0,1) != 'A' & this.accuracy.Accuracy1.reason_code.substring(0,1) != 'C' & this.accuracy.Accuracy1.reason_code.substring(0,1) != 'P' & this.accuracy.Accuracy1.reason_code.substring(0,1) != 'N' )
				{
					corr_non_fin = 1;
				}
				else
				{
					corr_fin = 1;
				}
				emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:0,correction_count_imports:corr_vol_imp,correction_count:corr_vol,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
				
			}
		}
		if (this.file_type === 'BB_TONNAGE')
		{
			if(this.file_num)
			{
				mawb_cnt = 1;
			}
			hawb_cnt = this.hawb_cnt;
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:0,correction_count_imports:corr_vol_imp,correction_count:corr_vol,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
		}
		
	}
	else
	{
		if (this.file_type === 'BB_Log_Open')
		{	
			log_vol = 1;
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:corr_vol,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
		}
		if (this.file_type === 'BB_Inv_Reg')
		{	
			accu_vol = 1;
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:corr_vol,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
		}
		if (this.file_type === 'BB_Inv_Acc')
		{
			corr_vol = 1;
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:corr_vol,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
		}
		if (this.file_type === 'BB_TONNAGE')
		{
			if(this.file_num)
			{
				mawb_cnt = 1;
			}
			hawb_cnt = this.hawb_cnt;
			emit({country:"us",region:this.region, station:this.station, branch:this.division_code, year:this.year, month:this.month}, {volume : log_vol,accuracy_volume:accu_vol,correction_count_bb:corr_vol_bb,correction_count_imports:corr_vol_imp,correction_count:corr_vol,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt});
		}
	
	}

	};
var red = function(key, values) {
	var log_vol_count = 0;
	var accu_vol_count = 0;
	var corr_count_imp = 0;
	var mawb_cnt = 0;
	var hawb_cnt = 0;
	var corr_fin = 0;
	var corr_non_fin = 0;
	var corr_count_bb = 0;	
	var corr_count_others = 0;
	var a,b,c;

values.forEach(function(doc) {
	log_vol_count += doc.volume;
	accu_vol_count += doc.accuracy_volume;
	mawb_cnt += doc.mawb_count;
	hawb_cnt += doc.hawb_count;
	corr_count_bb += doc.correction_count_bb;
	corr_fin += doc.correction_count_fatal;
	corr_non_fin += doc.correction_count_non_fatal;
	corr_count_others += doc.correction_count;
	corr_count_imp += doc.correction_count_imports;
});
		return {volume : log_vol_count,accuracy_volume:accu_vol_count,correction_count_bb:corr_count_bb,correction_count_imports:corr_count_imp,correction_count:corr_count_others,correction_count_fatal:corr_fin,correction_count_non_fatal:corr_non_fin,mawb_count:mawb_cnt,hawb_count:hawb_cnt};

};

var final = function(key,value) {    
	
	var corr_p = 0;
	var corr_fin_p = 0;
	var corr_non_fin_p = 0;
	
	if(key.branch === 'AI' | key.branch === 'OI')
	{
		if(value.hawb_count === 0)
			corr_p = 0;
		else
			corr_p = (value.correction_count_bb * 100)/value.hawb_count;
	}
	else if(key.branch === 'CA' | key.branch === 'CO')
	{
		if(value.accuracy_volume === 0)
		{
			corr_p = 0;
			corr_fin_p = 0;
			corr_non_fin_p = 0;
		}
		else
		{
			corr_p = (value.correction_count_imports * 100)/value.accuracy_volume;
			corr_fin_p = (value.correction_count_fatal * 100)/value.accuracy_volume;
			corr_non_fin_p = (value.correction_count_non_fatal * 100)/value.accuracy_volume;
		}	
	}
	else
	{
		if(value.accuracy_volume === 0)
			corr_p = 0;
		else
			corr_p = (value.correction_count * 100)/value.accuracy_volume;
	}
	return {volume : value.volume,
			accuracy_volume : value.accuracy_volume,
			correction_count_bb : value.correction_count_bb,
			correction_count_imports : value.correction_count_imports,
			correction_count : value.correction_count,
			mawb_count: value.mawb_count,
			hawb_count: value.hawb_count,
			correction_count_fatal: value.correction_count_fatal,
			correction_count_non_fatal: value.correction_count_non_fatal,
			corrected_per : 100 - corr_p,
			correction_per_fatal:100 - corr_fin_p,
			correction_per_non_fatal:100 - corr_non_fin_p};
}

var map1 = function(){

emit({country:this._id.country,region:this._id.region,  branch:this._id.branch, year:this._id.year, month:this._id.month}, {volume : this.value.volume,accuracy_volume:this.value.accuracy_volume,correction_count_bb:this.value.correction_count_bb,correction_count_imports:this.value.correction_count_imports,correction_count:this.value.correction_count,mawb_count:this.value.mawb_count,hawb_count:this.value.hawb_count,correction_count_fatal:this.value.correction_count_fatal,correction_count_non_fatal:this.value.correction_count_non_fatal});
};

var map2 = function(){

emit({country:this._id.country, branch:this._id.branch, year:this._id.year, month:this._id.month}, {volume : this.value.volume,accuracy_volume:this.value.accuracy_volume,correction_count_bb:this.value.correction_count_bb,correction_count_imports:this.value.correction_count_imports,correction_count:this.value.correction_count,mawb_count:this.value.mawb_count,hawb_count:this.value.hawb_count,correction_count_fatal:this.value.correction_count_fatal,correction_count_non_fatal:this.value.correction_count_non_fatal});
};


var curDateTime1 = new Date();
curDateTime1.setDate(curDateTime1.getDate() - 4);

var res = db.src_breakbulk_import_trend.mapReduce(map, red, {query : { "insert_date" : {$gte:curDateTime1}},finalize : final, out : { "merge" : "view_bb_import_trend_summary_station" }});
var res1 = db.view_bb_import_trend_summary_station.mapReduce(map1, red, {finalize : final, out : { "merge" : "view_bb_import_trend_summary_region" }});
var res2 = db.view_bb_import_trend_summary_region.mapReduce(map2, red, {finalize : final, out : { "merge" : "view_bb_import_trend_summary_country" }});

