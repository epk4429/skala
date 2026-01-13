// ============================================
// 개인 프로필 페이지 - JavaScript
// ============================================

// DOM이 로드된 후 실행
document.addEventListener('DOMContentLoaded', function() {
    // 스크롤 시 네비게이션 바 스타일 변경
    initNavbarScroll();
    
    // 폼 제출 처리
    initContactForm();
    
    // 스크롤 애니메이션
    initScrollAnimation();
    
    // 프로그레스 바 애니메이션
    initProgressBars();
});

// ============================================
// 네비게이션 바 스크롤 효과
// ============================================
function initNavbarScroll() {
    const navbar = document.querySelector('.custom-navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        // 스크롤 다운 시 네비게이션 바 투명도 조절
        if (currentScroll > 100) {
            navbar.style.backgroundColor = 'rgba(13, 110, 253, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.backgroundColor = '';
            navbar.style.backdropFilter = '';
        }

        lastScroll = currentScroll;
    });
}

// ============================================
// 연락처 폼 제출 처리
// ============================================
function initContactForm() {
    const form = document.getElementById('contact-form');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // 기본 제출 동작 방지
            
            // 폼 데이터 수집
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                subject: document.getElementById('subject').value,
                message: document.getElementById('message').value
            };
            
            // 간단한 유효성 검사
            if (!validateForm(formData)) {
                return;
            }
            
            // 성공 메시지 표시 (실제로는 서버로 전송)
            showSuccessMessage();
            
            // 폼 초기화
            form.reset();
        });
    }
}

// 폼 유효성 검사
function validateForm(data) {
    // 이름 검증
    if (data.name.trim() === '') {
        alert('이름을 입력해주세요.');
        document.getElementById('name').focus();
        return false;
    }
    
    // 이메일 검증
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(data.email)) {
        alert('올바른 이메일 형식을 입력해주세요.');
        document.getElementById('email').focus();
        return false;
    }
    
    // 제목 검증
    if (data.subject.trim() === '') {
        alert('제목을 입력해주세요.');
        document.getElementById('subject').focus();
        return false;
    }
    
    // 메시지 검증
    if (data.message.trim() === '') {
        alert('메시지를 입력해주세요.');
        document.getElementById('message').focus();
        return false;
    }
    
    return true;
}

// 성공 메시지 표시
function showSuccessMessage() {
    const form = document.getElementById('contact-form');
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success mt-3';
    successDiv.innerHTML = '<i class="bi bi-check-circle me-2"></i>메시지가 성공적으로 전송되었습니다!';
    
    // 기존 알림 제거
    const existingAlert = form.parentElement.querySelector('.alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    form.parentElement.appendChild(successDiv);
    
    // 3초 후 알림 제거
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// ============================================
// 스크롤 애니메이션
// ============================================
function initScrollAnimation() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // 애니메이션을 적용할 요소들
    const animateElements = document.querySelectorAll('.card, .skill-card, .contact-info');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// ============================================
// 프로그레스 바 애니메이션
// ============================================
function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    const observerOptions = {
        threshold: 0.5
    };
    
    const progressObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                
                // 초기값 0으로 설정
                progressBar.style.width = '0%';
                
                // 애니메이션으로 원래 값까지 증가
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 100);
                
                progressObserver.unobserve(progressBar);
            }
        });
    }, observerOptions);
    
    progressBars.forEach(bar => {
        progressObserver.observe(bar);
    });
}

// ============================================
// 부드러운 스크롤 (네비게이션 링크 클릭 시)
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        
        // 빈 해시(#)인 경우 무시
        if (href === '#') {
            return;
        }
        
        const target = document.querySelector(href);
        
        if (target) {
            e.preventDefault();
            
            const offsetTop = target.offsetTop - 80; // 네비게이션 바 높이 고려
            
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
            
            // 모바일에서 네비게이션 메뉴 닫기
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                bsCollapse.hide();
            }
        }
    });
});

// ============================================
// 현재 섹션에 따라 네비게이션 활성화
// ============================================
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// ============================================
// 프로젝트 카드 클릭 이벤트 (예제)
// ============================================
document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('click', function(e) {
        // 버튼이 아닌 카드 영역을 클릭했을 때만
        if (!e.target.closest('.btn')) {
            console.log('프로젝트 카드 클릭됨:', this.querySelector('.card-title').textContent);
            // 여기에 상세 페이지로 이동하는 로직 추가 가능
        }
    });
});

// ============================================
// 소셜 링크 클릭 이벤트 (예제)
// ============================================
document.querySelectorAll('.social-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const platform = this.getAttribute('title');
        console.log(`${platform} 링크 클릭됨`);
        // 실제 링크로 이동하는 로직 추가
        // window.open('실제 URL', '_blank');
    });
});
