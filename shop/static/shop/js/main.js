(function($) {
	function getCookie(c_name)
	{
		if (document.cookie.length > 0)
		{
			let c_start = document.cookie.indexOf(c_name + "=");
			if (c_start != -1)
			{
				c_start = c_start + c_name.length + 1;
				let c_end = document.cookie.indexOf(";", c_start);
				if (c_end == -1) c_end = document.cookie.length;
				return unescape(document.cookie.substring(c_start,c_end));
			}
		}
		return "";
	 }
	$.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });


	"use strict"

	// Mobile Nav toggle
	$('.menu-toggle > a').on('click', function (e) {
		e.preventDefault();
		$('#responsive-nav').toggleClass('active');
	})

	// Fix cart dropdown from closing
	$('.cart-dropdown').on('click', function (e) {
		e.stopPropagation();
	});

	/////////////////////////////////////////

	// products Slick
	$('.products-slick').each(function() {
		var $this = $(this),
				$nav = $this.attr('data-nav');

		$this.slick({
			slidesToShow: 4,
			slidesToScroll: 1,
			autoplay: true,
			infinite: true,
			speed: 300,
			dots: false,
			arrows: true,
			appendArrows: $nav ? $nav : false,
			responsive: [{
	        breakpoint: 991,
	        settings: {
	          slidesToShow: 2,
	          slidesToScroll: 1,
	        }
	      },
	      {
	        breakpoint: 480,
	        settings: {
	          slidesToShow: 1,
	          slidesToScroll: 1,
	        }
	      },
	    ]
		});
	});

	// products Widget Slick
	$('.products-widget-slick').each(function() {
		var $this = $(this),
				$nav = $this.attr('data-nav');

		$this.slick({
			infinite: true,
			autoplay: true,
			speed: 300,
			dots: false,
			arrows: true,
			appendArrows: $nav ? $nav : false,
		});
	});

	/////////////////////////////////////////

	// Product Main img Slick
	$('#product-main-img').slick({
    infinite: true,
    speed: 300,
    dots: false,
    arrows: true,
    fade: true,
    asNavFor: '#product-imgs',
  });

	// Product imgs Slick
  $('#product-imgs').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: true,
    centerMode: true,
    focusOnSelect: true,
		centerPadding: 0,
		vertical: true,
    asNavFor: '#product-main-img',
		responsive: [{
        breakpoint: 991,
        settings: {
					vertical: false,
					arrows: false,
					dots: true,
        }
      },
    ]
  });

	// Product img zoom
	var zoomMainProduct = document.getElementById('product-main-img');
	if (zoomMainProduct) {
		$('#product-main-img .product-preview').zoom();
	}

	/////////////////////////////////////////

	// Input number
	$('.input-number').each(function() {
		var $this = $(this),
		$input = $this.find('input[type="number"]'),
		up = $this.find('.qty-up'),
		down = $this.find('.qty-down');

		down.on('click', function () {
			var value = parseInt($input.val()) - 1;
			value = value < 1 ? 1 : value;
			$input.val(value);
			$input.change();
		})

		up.on('click', function () {
			var value = parseInt($input.val()) + 1;
			$input.val(value);
			$input.change();
		})
	});

	if ($('#price-max').length > 0 && $('#price-min').length > 0) {
		var priceInputMax = document.getElementById('price-max'),
				priceInputMin = document.getElementById('price-min');
		priceInputMax.addEventListener('change', function () {
			updatePriceSlider($(this).parent(), this.value)
		});

		priceInputMin.addEventListener('change', function () {
			updatePriceSlider($(this).parent(), this.value)
		});

		function updatePriceSlider(elem, value) {
			if (elem.hasClass('price-min')) {
				console.log('min')
				priceSlider.noUiSlider.set([value, null]);
			} else if (elem.hasClass('price-max')) {
				console.log('max')
				priceSlider.noUiSlider.set([null, value]);
			}
		}

		// Price Slider
		var priceSlider = document.getElementById('price-slider');
		if (priceSlider) {
			noUiSlider.create(priceSlider, {
				start: [1, 999],
				connect: true,
				step: 1,
				range: {
					'min': 1,
					'max': 999
				}
			});

			priceSlider.noUiSlider.on('update', function (values, handle) {
				var value = values[handle];
				handle ? priceInputMax.value = value : priceInputMin.value = value
			});
		}
	}

	$('div.cart-list > div.product-widget > button.delete').each(function (){
		$(this).on('click', function (){
		let dataId = $(this).attr('data-object-id');
		deleteCartProduct(dataId);
	})
	})

	function deleteCartProduct(id) {
		let url = $("#capt-product-delete").attr("data-url");
		$.ajax({
			url: url,
			type: 'POST',
			data: {
				'id': id,
			},
			dataType: 'json',
			success: function (data) {
				if (data['total_products'] > 0) {
					$(`button.delete[data-object-id=${id}]`).parent().remove();

					$('#cart a div.qty').text(data['total_products']);

					let cart_summary_total_products = $('div.cart-summary small');
					let total_products_splitted_text = cart_summary_total_products.text().split(' ');
					total_products_splitted_text[0] = data['total_products']
					cart_summary_total_products.text(total_products_splitted_text.join(' '));

					let cart_summary_total_price = $('div.cart-summary h5');
					let total_price_splitted_text = cart_summary_total_price.text().split('₴');
					total_price_splitted_text[1] = data['total_price'].replace('.', ',');
					cart_summary_total_price.text(total_price_splitted_text.join('₴'));
				}
				else {
					$('#cart a div.qty').remove();
					$('#cart div.cart-dropdown div.cart-list').remove();
					$('#cart div.cart-dropdown div.cart-summary').replaceWith('<h4>Корзина пуста</h4>');
				}
			},
			error: function(data) {
                console.log(`${data['statusText']}(${data['status']}): ${data['responseJSON']['message']}`);
			}
		});
	}

})(jQuery);
