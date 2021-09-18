$(document).ready(function(){

//회원가입버튼 클릭 후 로그인 박스가 회원가입 박스로 변경
$('#goToSignUp').click(function(){

    //박스 크기 변경 
    $('#box').animate({
        height:'409px'
    });

    //로그인 내용물은 흐리게 사라지기
    $('#signIn').fadeOut();

    //회원가입 내용물이 아예 숨겨지면 회원가입 내용물 보이기
    if($('#signIn').hide()){$('#signUp').fadeIn(800);}
});

//뒤로가기 버튼 클릭 후 다시 로그인 박스로 변경
$('#signUp .back').click(function(){

    //박스 크기 변경
    $('#box').animate({
        height:'353px'
    });

    //회원가입 내용물 흐리게 사라지기
    $('#signUp').fadeOut();

    //회원가입 내용물이 아예 숨겨지면 로그인 내용물 보이기
    if($('#signUp').hide()){$('#signIn').fadeIn(800);}
    
});


// 회원가입창에서 값 입력시 경고문 해제
$('.suID input').on("change keyup paste", function(){
    $('.suID .wrong').text('');
})
$('.suPW input').on("change keyup paste", function(){
    $('.suPW .wrong').text('');
})

});