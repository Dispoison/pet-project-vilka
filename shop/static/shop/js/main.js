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

	// Fix wishlist dropdown from closing
	$('.wishlist-dropdown').on('click', function (e) {
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

	let rating = 0;
	$('input[name=rating]').each(function (){
		$(this).on('click', function (){
			rating = $(this).attr('value')
		})
	})


	$('#review-form .primary-btn').on('click', function (){
		if (rating > 0 && rating <= 5){
			let text = $(this).siblings('textarea').val();
			sendReview($(this), text);
		}
		else {
			console.error('Недопустимое значение рейтинга: ' + rating);
		}
	})

	function changeStarsCount(total_count, stars_counts){
		let stars_countainer = $('div#rating > ul.rating')

		for (let i = 5; i > 0; --i){
			stars_countainer.children(`li[data-stars=${i}]`).children('span.sum').text(stars_counts[i])
			let percent = total_count === 0 ? '0%' : (stars_counts[i] / total_count * 100).toString() + '%'
			stars_countainer.children(`li[data-stars=${i}]`).children('div.rating-progress').children('div').css('width', percent)
		}
	}

	function fillStars(rating){
		let text = ""
		let full_stars = parseInt(rating)
		let remainder = parseFloat(rating) - full_stars
		let half_star = 0
		if (0.5 <= remainder){
			half_star = 1
		}
		let empty_stars = 5 - (full_stars + half_star)

		for (let i = 0; i < full_stars; ++i){
			text += '<i class="fa fa-star"></i>\n'
		}
		if (half_star === 1){
			text += '<i class="fa fa-star-half-full"></i>\n'
		}
		for (let i = 0; i < empty_stars; ++i){
			text += '<i class="fa fa-star-o"></i>\n'
		}
		return text
	}

	function sendReview(btn, text){
		$.ajax({
			url: btn.attr('data-create-url'),
			type: 'POST',
			data: {
				'product-id': btn.attr('data-id'),
				'rating': rating,
				'text': text,
			},
			dataType: 'json',
			success: function (data) {
				let ul_reviews = $('ul.reviews')
				let text = "<li>\n" +
						   "<div class=\"review-heading\">\n" +
						   `        <h5 class=\"name\">${data['username']}</h5>\n` +
						   `        <p class=\"date\">${data['created_at']}</p>\n` +
						   "        <div class=\"review-rating\">\n" +
										starCalculate(data['rating']) +
						   "        </div>\n" +
						   "    </div>\n" +
						   "    <div class=\"review-body\">\n" +
						   `        <p>${data['text']}</p>\n` +
						   "    </div>\n" +
						 "</li>"


				let total_stars_count = data['total_stars_count']

				let reviewLink = $('a.review-link')
				reviewLink.text(total_stars_count + ' ' + reviewLink.text().split(' ').slice(1).join(' '))

				let tabReviews = $('#tab-reviews')
				tabReviews.text(tabReviews.text().split(' ')[0] + ` (${total_stars_count})`)

				let ratingStars = $('div#rating div.rating-avg div.rating-stars')
				ratingStars.empty()
				ratingStars.append(fillStars(data['product_rating']))


				$('div.rating-avg > span').text(data['product_rating'])
				let stars_counts = {
					5: data['five_star_count'],
					4: data['four_star_count'],
					3: data['three_star_count'],
					2: data['two_star_count'],
					1: data['one_star_count'],
				}
				changeStarsCount(total_stars_count, stars_counts)

				$('div#reviews p.reviews-empty').remove()

				ul_reviews.prepend(text)
			},
			error: function(data) {
                console.log(`${data['statusText']}(${data['status']}): ${data['responseJSON']['message']}`);
			}
		});
	}

	$('a.review-link').on('click', function (){
		$('#tab-reviews').trigger('click')
		$('html,body').animate({scrollTop: $('.tab-nav').offset().top});
	})

	$('button.more-reviews-btn').on('click', function (){
		let earlisestReview = $('.earliest-review');

		let url = $(this).parent('div#reviews').attr('data-more-url')
		let productId = $(this).parent('div#reviews').attr('data-product-id');
		let earliestReviewId = earlisestReview.attr('data-review-id');

		earlisestReview.removeClass('earliest-review');
		earlisestReview.removeAttr('data-review-id')

		getMoreReviews(url, productId, earliestReviewId)
	})

	function starCalculate(rating){
		let text = ""
		for (let i = 1; i <= 5; ++i){
			if (i <= rating){
				text += "<i class=\"fa fa-star\"></i>\n"
			}
			else{
				text += "<i class=\"fa fa-star-o empty\"></i>\n"
			}
		}
		return text
	}

	function getMoreReviews(url, productId, earliestReviewId){
		$.ajax({
			url: url,
			type: 'GET',
			data: {
				'product_id': productId,
				'earliest_review_id': earliestReviewId,
			},
			dataType: 'json',
			success: function (data) {
				let ul_reviews = $('ul.reviews')
				let reviews = data['reviews'];

				for (let i = 0; i < reviews.length; ++i){
					let text = ""

					if (reviews[i]['earliest-review']) {
						text += `<li class=\"earliest-review\" data-review-id=\"${reviews[i]['review_id']}\">\n`}
					else {
						text += "<li>\n" }

					text +=    "    <div class=\"review-heading\">\n" +
						       `        <h5 class=\"name\">${reviews[i]['username']}</h5>\n` +
						       `        <p class=\"date\">${reviews[i]['created_at']}</p>\n` +
						       "        <div class=\"review-rating\">\n" +
											starCalculate(reviews[i]['rating']) +
						       "        </div>\n" +
						       "    </div>\n" +
						       "    <div class=\"review-body\">\n" +
						       `        <p>${reviews[i]['text']}</p>\n` +
						       "    </div>\n" +
						       "</li>"
					ul_reviews.append(text)
				}

				if (data['nothing_else']){
					$('button.more-reviews-btn').remove()
				}
			},
			error: function(data) {
                console.log(`${data['statusText']}(${data['status']}): ${data['responseJSON']['message']}`);
			}
		});
	}

})(jQuery);
