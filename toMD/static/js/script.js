$.fn.extend({
	txtaAutoHeight: function () {
		return this.each(function () {
			var $this = $(this);
		   if (!$this.attr('initAttrH')) {
				$this.attr('initAttrH', $this.outerHeight());
			}
			setAutoHeight(this).on('input', function () {
				setAutoHeight(this);
			});
		});
		function setAutoHeight(elem) {
			var $obj = $(elem);
			return $obj.css({ height: $obj.attr('initAttrH'), 'overflow-y': 'hidden' }).height(elem.scrollHeight);
		}
	}
});

 $(function(){
    $("#div1").css("opacity","0.3");   //设置透明度
 });

$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }
    $('[data-toggle="tooltip"]').tooltip(
        {title: render_time}
    );
});

//闭包自增
function getId () {
  'use strict';

  var i = 0;
  getId = function () {
    return i++;
  };
  return i++;

}

//Set cookie
function doCookieSetup(name, value) {
  var expibonus = new Date();
  //有效時間保存 1 天 24*60*60*1000
  expibonus.setTime(expibonus.getTime() + 172800000);
  document.cookie = name + "=" + escape(value) + ";expibonus=" + expibonus.toGMTString()
}

function listCookie() {
  document.writeln("<table>");
  document.writeln("<tr><th>Name<th>Value");
  cookieArray = document.cookie.split(";");
  for (var i = 0; i < cookieArray.length; i++) {
    thisCookie = cookieArray[i].split("=");
    cName = unescape(thisCookie[0]);
    cValue = unescape(thisCookie[1]);
    document.writeln("<tr><td>" + cName + "</td><td>" + cValue + "</td>");
  }
  document.writeln("</table>");
}

