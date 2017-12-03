
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
   'productName' : 'MouZhiA',
	 'copyRight' : '2017 CSC326UltimateTeam',
	 'languageText' : 'Language:',
	 'slogan': 'Constantly strive for perfection.',
	 'teamName' : '--CSC326UltimateTeam',
	 'email': 'Email Us',
	 'hiStranger': 'Hi Stranger!',
	 'signIn': 'Sign In',
	 'account': 'Log In With Google',
	 'didMean': 'Did you mean',
	 'showingResults': 'Showing results for',
	 'searchInstead': 'Search Instead for',
	 'previous': 'Previous',
		'next': 'Next',
		'thatsError': "That's an error.",
    'pageNotFound': "The requested URL / rustybrick was not found on this server.",
		'yourSearch' : "Your search",
		'notMatching': "did not match any documents",
		'suggestionTitle' : 'Suggestions:',
		'suggestionOne': 'Make sure that all words are spelled correcly',
		'suggestionTwo': 'Try different keywords',
		'suggestionThree': 'Try more general keywords',
		'suggestionFour': 'Try fewer keywords',
		'Aboutresult' : 'About',
		'aboutResult': 'results',
		'preview': 'Preview',
		'closeBtn' : 'Close',
		'signOut' : 'Sign Out'
	},
	'zh': {
		'about': '关于',
		'productName' : '冇知啊',
		'copyRight' : '2017 CSC326终极小队',
		 'languageText' : '语言:',
		  'slogan': '持续追求完美',
			'teamName' : '--CSC326终极小队',
			'email': 'Email 我们',
			 'hiStranger': '你好 陌生人!',
			 'signIn': '登陆',
			 'account': '通过google登陆',
			 'didMean': '您是不是要找',
			 'showingResults': '显示已更正搜索结果',
			  'searchInstead': '然而不听话的您依然坚持搜索',
				'previous': '上一页',
				'next': '下一页',
				'thatsError': '出问题了!',
				'pageNotFound': "求求你别问我。我也找不到你要的网页。",
				'yourSearch' : "您所搜索的词条",
				'notMatching': "无法在数据库中搜索到",
				'suggestionTitle': '给您的几个忠告：',
				'suggestionOne': '请确认所有搜索词条拼写正确',
				'suggestionTwo': '实践是检验真理的唯一标准。试试其他的搜索词条吧',
				'suggestionThree': '停止标新立异，尝试搜索更加常见的词条',
				'suggestionFour': '求求你别累死我了，请减少搜索的词条的长度',
				'Aboutresult': '大约有',
				'aboutResult': '个搜索结果',
				'preview': '冇知快照',
				'closeBtn' : '关闭',
				'signOut' : '退出'
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
