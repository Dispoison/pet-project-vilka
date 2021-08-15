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
			$input.attr('value', value)
		})

		up.on('click', function () {
			var value = parseInt($input.val()) + 1;
			$input.val(value);
			$input.change();
			$input.attr('value', value)
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

	/*
			Cart
	 */

	$('#cart div.cart-list > div.product-widget > button.delete').each(function (){
		$(this).on('click', function (){
		let dataId = $(this).attr('data-object-id');
		deleteCartProduct(dataId);
	})
	})

	function updateCart(data){
		let quantity = $('#cart a div.qty')
		if (quantity.length){
			quantity.text(data['total_products']);
		}
		else{
			let qty_parent = $('#cart a.dropdown-toggle');
			qty_parent.append(`<div class=\"qty\">${data['total_products']}</div>`)
		}

		let cartSummaryTotalProducts = $('div.cart-summary small');
		let totalProductsSplittedText = cartSummaryTotalProducts.text().split(' ');
		totalProductsSplittedText[0] = data['total_products']
		cartSummaryTotalProducts.text(totalProductsSplittedText.join(' '));

		let cartSummaryTotalPrice = $('div.cart-summary h5');
		let totalPriceSplittedText = cartSummaryTotalPrice.text().split('₴');
		totalPriceSplittedText[1] = data['total_price'].replace('.', ',');
		cartSummaryTotalPrice.text(totalPriceSplittedText.join('₴'));
	}

	function deleteCartProduct(id) {
		$.ajax({
			url: $('#cart').attr('data-delete-url'),
			type: 'POST',
			data: {
				'id': id,
			},
			dataType: 'json',
			success: function (data) {
				if (data['total_products'] > 0) {
					$(`#cart button.delete[data-object-id=${id}]`).parent().remove();

					updateCart(data);
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

	$('div.add-to-cart > button.add-to-cart-btn').each(function (){
		$(this).on('click', function (){
			let id = $(this).attr("data-id");
			let quantity;
			let product_url = $(this).attr('data-product-url');
			let product_name;
			let photo_url;

			if ($(`button.add-to-cart-btn[data-id=${id}]`).parent('div.add-to-cart').parent('div.product').length) {
				quantity = 1;
				product_name = $(this).parent('div.add-to-cart').siblings('div.product-body').find('h3.product-name a').text();
				photo_url = $(this).closest('div.product').find('a div.product-img img').attr('src');
			}
			else{
				quantity = $('div.add-to-cart div.input-number > input#quantity').attr('value');
				product_name = $('h2.product-name').text();
				photo_url = $('div.product-preview img').first().attr('src');
			}

			createCartProduct(id, quantity, product_url, product_name, photo_url);
		})
	})

	function createCartProduct(id, quantity, product_url, product_name, photo_url) {
		$.ajax({
			url: $('#cart').attr('data-create-url'),
			type: 'POST',
			data: {
				'id': id,
				'quantity': quantity,
			},
			dataType: 'json',
			success: function (data) {
				let cart_product_total_price = data['cart_product_total_price'];
				let cart_product_id = data['cart_product_id'];
				let total_quantity = data['total_quantity'];

				switch (data['result']) {
					case 'created':

						let cart_list = $('div.cart-list');

						if (cart_list.length === 0){
							let cart_dropdown = $('#cart div.cart-dropdown');
							cart_dropdown.children('h4').remove()
							cart_dropdown.prepend("<div class=\"cart-summary\"></div>")
							cart_dropdown.prepend("<div class=\"cart-list\"></div>")

							cart_dropdown.children('div.cart-summary').append("<small>0 Продуктов выбрано</small>\n" +
								"                <h5>СУММА: ₴0</h5>")
							cart_list = cart_dropdown.children('div.cart-list');
						}

						cart_list.append("<div class=\"product-widget\">\n" +
							"                    <div class=\"product-img\">\n" +
							`                        <img src=\"${photo_url}\" alt=\"\">\n` +
							"                    </div>\n" +
							"                    <div class=\"product-body\">\n" +
							`                        <h3 class=\"product-name\"><a href=\"${product_url}\">${product_name}</a></h3>\n` +
							`                        <h4 class=\"product-price\"><span class=\"qty\">${total_quantity}x</span>₴${cart_product_total_price}</h4>\n` +
							"                    </div>\n" +
							`                    <button class=\"delete\" data-object-id=\"${cart_product_id}\"><i class=\"fa fa-close\"></i></button>\n` +
							"                </div>");

						let button = $(`button.delete[data-object-id=${cart_product_id}]`)
						button.on('click', function (){
							let dataId = $(this).attr('data-object-id');
							deleteCartProduct(dataId);
						})

						updateCart(data);
						break;
					case 'updated':
						let product_price = $(`#cart button.delete[data-object-id=${cart_product_id}]`).siblings('div.product-body').children('h4.product-price')
						product_price.text(`₴${cart_product_total_price}`)
						product_price.prepend(`<span class="qty">${total_quantity}x</span>`)
						updateCart(data);
						break;
				}
			},
			error: function(data) {
                console.log(`${data['statusText']}(${data['status']}): ${data['message']}`);
			}
		});
	}

	/*
			Wishlist
	 */

	$('#wishlist div.wishlist-list > div.product-widget > button.delete').each(function (){
		$(this).on('click', function (){
		let dataId = $(this).attr('data-object-id');
		deleteWishlistProduct(dataId);
	})
	})

	function updateWishlist(data){
		let quantity = $('#wishlist a div.qty')
		if (quantity.length){
			quantity.text(data['total_products']);
		}
		else{
			let qty_parent = $('#wishlist a.dropdown-toggle');
			qty_parent.append(`<div class=\"qty\">${data['total_products']}</div>`)
		}
	}

	function deleteWishlistProduct(id) {
		$.ajax({
			url: $('#wishlist').attr('data-delete-url'),
			type: 'POST',
			data: {
				'id': id,
			},
			dataType: 'json',
			success: function (data) {
				if (data['total_products'] > 0) {
					$(`#wishlist button.delete[data-object-id=${id}]`).parent().remove();

					updateWishlist(data);
				}
				else {
					$('#wishlist a div.qty').remove();
					$('#wishlist div.wishlist-dropdown div.wishlist-list').replaceWith('<h4>Желаемого нет</h4>');
				}
			},
			error: function(data) {
                console.log(`${data['statusText']}(${data['status']}): ${data['responseJSON']['message']}`);
			}
		});
	}

	$('.add-to-wishlist').each(function (){
		$(this).on('click', function (){
			let id = $(this).attr("data-id");
			let product_url = $(this).attr('data-product-url');
			let product_name;
			let photo_url;

			if ($(this).is('button'))  {
				product_name = $(this).parent('div.product-btns').siblings('h3.product-name').children('a').text();
				photo_url = $(this).closest('div.product').find('a div.product-img img').attr('src');
			}
			else if ($(this).is('div')) {
				product_name = $('h2.product-name').text();
				photo_url = $('div.product-preview img').first().attr('src');
			}

			createWishlistProduct(id, product_url, product_name, photo_url);
		})
	})

	function createWishlistProduct(id, product_url, product_name, photo_url) {
		$.ajax({
			url: $('#wishlist').attr('data-create-url'),
			type: 'POST',
			data: {
				'id': id,
			},
			dataType: 'json',
			success: function (data) {
				let wishlist_product_id = data['wishlist_product_id'];

				let wishlist_list = $('div.wishlist-list');

				if (wishlist_list.length === 0){
					let wishlist_dropdown = $('#wishlist div.wishlist-dropdown');
					wishlist_dropdown.children('h4').remove()
					wishlist_dropdown.prepend("<div class=\"wishlist-list\"></div>")

					wishlist_list = wishlist_dropdown.children('div.wishlist-list');
				}

				wishlist_list.append("<div class=\"product-widget\">\n" +
					"                    <div class=\"product-img\">\n" +
					`                        <img src=\"${photo_url}\" alt=\"\">\n` +
					"                    </div>\n" +
					"                    <div class=\"product-body\">\n" +
					`                        <h3 class=\"product-name\"><a href=\"${product_url}\">${product_name}</a></h3>\n` +
					"                    </div>\n" +
					`                    <button class=\"delete\" data-object-id=\"${wishlist_product_id}\"><i class=\"fa fa-close\"></i></button>\n` +
					"                </div>");

				let button = $(`button.delete[data-object-id=${wishlist_product_id}]`)
				button.on('click', function (){
					let dataId = $(this).attr('data-object-id');
					deleteWishlistProduct(dataId);
				})

				updateWishlist(data);
			},
			error: function(data) {
                console.log(`${data['statusText']}(${data['status']}): ${data['responseJSON']['message']}`);
			}
		});
	}


})(jQuery);
