$(document).ready(function () {

    //옵션페이지에서 마우스 올라가면 귀엽게 변경
    $('#enter').mouseover(function () {
        $('#character img').attr('src', '../static/img/cuteCHAR.svg');
        $(this).addClass('buttonGradientAni');
    });
    //마우스 내려가면 원래대로
    $('#enter').mouseout(function () {
        $('#character img').attr('src', '../static/img/CHAR.svg');
        $(this).removeClass('buttonGradientAni');
    });

    //고정단어 옵션
    let wordOption = $('.wordOption p');
    //고정단어 종류 클릭 시
    $(wordOption).click(function () {

        //클릭한 것은 on 그 외의 형재태그는 off 를 가져서 구분할 수 있도록 하기
        if ($(this).hasClass('off')) {
            $(this)
                .removeClass('off')
                .addClass('on');
            $(this)
                .siblings('p')
                .addClass('off')
                .removeClass('on');
        }

        //형용사를 체크했을 때 명사종류 창을 보이게 하고 그게 아니라면 명사종류 창 안보이게 하기 css로 제어
        if ($('#optionCheck').hasClass('on')) {
            $('.nounOption').removeClass('clickNoun');
        } else {
            $('.nounOption').addClass('clickNoun');
        }

        //입력창 초기화
        $('#ex_input').val('');
        $('#ex_input').focus();
        $('#ex_input').focusout();

        //클릭한 것 종류의 명칭 가져오기
        let word = $(this).text();

        //고정단어 종류에 따라 input박스 안 택스트 다르게
        if (word == '완전랜덤') {
            let labelText = `완전랜덤으로 내 이름을 정해줘!`;
            $("label[for='ex_input']").text(labelText);
            $('#ex_input').attr('readonly', true);
            //완전랜덤일경우 input박스 클릭 막기
            $('.textInput').addClass('NoClick');
        } else {
            let labelText = `${word}를 원해!`;
            $("label[for='ex_input']").text(labelText);
            $('#ex_input').attr('readonly', false);
            $('.textInput').removeClass('NoClick');
        }

    });

    //고정단어 input 설정
    let input = $(' .textInput input')
    //focus on
    input.on('focus', function () {
        if ($(this).siblings('label') != null && $('.wordOption p:last-child').hasClass('off')) {
            $(this)
                .siblings('label')
                .css('opacity', 0);
        }
        if ($('.wordOption p:last-child').hasClass('off')) {
            $(this)
                .siblings('.textClear')
                .css('display', 'block');
        }
    });

    //focus out
    input.on('focusout', function () {
        if ($(this).val() == '' && $(this).siblings('label') != null) {
            $(this)
                .siblings('label')
                .css('opacity', '80%');
            $(this)
                .siblings('.textClear')
                .css('display', 'none');
        }
    });

    //input text clear
    $(' .textClear').click(function () {
        $(this)
            .siblings('input')
            .val('');
        $(this)
            .siblings('label')
            .click();
    });

    //체크박스 클래스 추가+제거
    $('.checks input').click(function () {

        if ($(this).hasClass('on')) {
            $(this).removeClass('on');
            $(this).addClass('off');
        } else {
            $(this).removeClass('off');
            $(this).addClass('on');
        }
    });

    //Result Page
    $('#saveName').hide();

    //저장하기
    $('.saveToMyPage').click(function () {
        $('#saveName').css('display', 'flex');
    });

    //저장 알림창 닫기
    $('#box .close').click(function () {
        $('#saveName').fadeOut();
        $('#saveName').hide();

    });

    //복사

    $('.Reset').click(function () {
        location.reload();
    });

});