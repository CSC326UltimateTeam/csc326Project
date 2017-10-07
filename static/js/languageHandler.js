
var language;
//load language from cookie
function loadLanguage() {
	language = getLanguage();
	//if language not set, set it to english
	if ( language != 'en' && language != "zh" ) {
		language = 'en';
	}
	//apply language
	applyLanguage();
}

//use cookie to save language
function saveLanguage( language ) {
	eraseCookie( "language" );
	createCookie( "language", language, 180 );
}
//read language from cookie
function getLanguage() {
	return readCookie( "language" );
}
//dictionary for language replacement
var arrLang = {
	'en': {
		'about': 'About',
		'account': 'Account',
   'productName' : 'MouZhiA',
	 'copyRight' : '2017 CSC326UltimateTeam',
	 'languageText' : 'Language:'
	},
	'zh': {
		'about': '关于',
		'account': '账户',
		'productName' : '冇知啊',
		'copyRight' : '2017 CSC326终极小队',
		 'languageText' : '语言:'
	}
};
//function to apply language
function applyLanguage() {
	//change language select box option
	if ( language == "en" ) {
		document.getElementById( "changeLang" )
			.selectedIndex = 0;
	} else {
		document.getElementById( "changeLang" )
			.selectedIndex = 1;
	}
	//jquery to replace words corresponding to arrLang regarding current language
	$( '.lang' )
		.each( function() {
			$( this )
				.text( arrLang[ language ][ $( this )
					.attr( 'key' ) ] );
		} );
		//change value of search button (english or chinese)
 $('.searchButton')
 .each( function() {
	 if ( language == 'en' ) {
		 $( this )
			 .attr( 'value', 'Search' );
	 } else {
		 $( this )
			 .attr( 'value', '搜索' );
	 }
 } );

}

//function to change language in language select box
function languageChange() {
//get selected value from selection box
	var selected_value = document.getElementById( 'changeLang' )
		.value;
	language = selected_value;
	//save language
	saveLanguage( language );
	console.log( language );
	//apply language
	applyLanguage();
}
