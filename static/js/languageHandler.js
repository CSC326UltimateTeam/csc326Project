var language;

function loadLanguage() {
	language = getLanguage();
	console.log( language );
	if ( language != 'en' && language != "zh" ) {
		language = 'en';
	}
	console.log( language );
	applyLanguage();
}

function saveLanguage( language ) {
	eraseCookie( "language" );
	createCookie( "language", language, 180 );
}

function getLanguage() {
	return readCookie( "language" );
}
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

function applyLanguage() {
	//change select box
	if ( language == "en" ) {
		document.getElementById( "changeLang" )
			.selectedIndex = 0;
	} else {
		document.getElementById( "changeLang" )
			.selectedIndex = 1;
	}
	$( '.lang' )
		.each( function() {
			$( this )
				.text( arrLang[ language ][ $( this )
					.attr( 'key' ) ] );
		} );
		if (document.getElementsByName("searchButton")[0]!=undefined) {
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
/**
if(document.getElementsByName("searchBar")[0] != undefined){
	$('.searchBar')
	.each( function() {
		if ( language == 'en' ) {
			$( this )
				.attr( 'placeholder', 'Enter Keywords' );
		} else {
			$( this )
				.attr( 'placeholder', '请输入关键词' );
		}
	} );
}**/
}


function languageChange() {
	var selected_value = document.getElementById( 'changeLang' )
		.value;
	language = selected_value;
	saveLanguage( language );
	console.log( language );
	applyLanguage();
}
