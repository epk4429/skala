const books = [
	{
		title: "자바스크립트 완벽 가이드",
		author: "David Flanagan",
		price: 35000,
		stock: 5,
		category: "프로그래밍",
		image: "./images/js-guide.jpg"
	},
	{
		title: "모던 자바스크립트 Deep Dive",
		author: "이웅모",
		price: 40000,
		stock: 0,
		category: "프로그래밍",
		image: "./images/js-deep-dive.jpg"
	},
	{
		title: "돈의 심리학",
		author: "모건 하우절",
		price: 18000,
		stock: 0,
		category: "경제",
		image: "./images/psychology-of-money.jpg"
	},
	{
		title: "불변의 법칙",
		author: "김동영",
		price: 14500,
		stock: 2,
		category: "소설",
		image: "./images/immutable-law.jpg"
	}
];


function showBooklist(){
    const btnLoadBooks = document.getElementById("btnLoadBooks");
    const bookListBox = document.getElementById("bookListBox");
    const bookListBody = bookListBox.querySelector(".card-body");

    btnLoadBooks.addEventListener("click", () => {

        bookListBody.innerHTML = "";
        let html = "";

        for (let i = 0; i < books.length; i++) {
            const book = books[i];

            const imgSrc = book.image
                ? book.image
                : "https://via.placeholder.com/80x110?text=No+Image";

            html += `
                <div class="d-flex gap-3 align-items-center border rounded p-2 mb-2">
                    <img
                        src="${imgSrc}"
                        alt="${book.title}"
                        class="rounded border"
                        style="width:80px; height:110px; object-fit:cover;"
                    />
                    <div class="fw-semibold">${book.title}</div>
                </div>
            `;
        }

        bookListBody.innerHTML = html;
    });
}
showBooklist();




function onStockBookList() {
    const btnOnStockBooks = document.getElementById("btnOnStockBooks");
    const box = document.getElementById("OnStockbookListBox");
    const body = box.querySelector(".card-body");

    btnOnStockBooks.addEventListener("click", () => {
 
        body.innerHTML = "";

        let html = "";
        let has = false;

        for (const book of books) {
            if (book.stock >= 1) {
                has = true;

                const imgSrc = book.image
                    ? book.image
                    : "https://via.placeholder.com/80x110?text=No+Image";

                html += `
                    <div class="d-flex gap-3 align-items-center border rounded p-2 mb-2">
                        <img
                            src="${imgSrc}"
                            alt="${book.title}"
                            class="rounded border"
                            style="width:80px; height:110px; object-fit:cover;"
                        />
                        <div class="flex-grow-1">
                            <div class="fw-semibold">${book.title}</div>
                            <div class="small text-muted">
                                가격: ${book.price.toLocaleString()}원 · 재고: ${book.stock}권
                            </div>
                        </div>
                    </div>
                `;
            }
        }

        body.innerHTML = html;
    });
}
onStockBookList();



function programmingBookList() {
    const btnProgrammingBooks = document.getElementById("btnProgrammingBooks");
    const box = document.getElementById("programmingBookListBox");
    const body = box.querySelector(".card-body");

    btnProgrammingBooks.addEventListener("click", () => {

        body.innerHTML = "";
        let html = "";
        let has = false;

        books.forEach((book) => {
            if (book.category === "프로그래밍") {
                has = true;

                const imgSrc = book.image
                    ? book.image
                    : "https://via.placeholder.com/80x110?text=No+Image";

                html += `
                    <div class="border rounded p-3 mb-2">
                        <div class="d-flex gap-3 align-items-center">
                            <img
                                src="${imgSrc}"
                                alt="${book.title}"
                                class="rounded border"
                                style="width:80px; height:110px; object-fit:cover;"
                            />
                            <div class="flex-grow-1">
                                <div class="fw-semibold mb-1">${book.title}</div>
                                <div class="small text-muted">
                                    author: ${book.author}<br/>
                                    category: ${book.category}<br/>
                                    price: ${book.price.toLocaleString()}원<br/>
                                    stock: ${book.stock}권<br/>
                                    image: ${book.image}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
        });

        body.innerHTML = html;
    });
}
programmingBookList();


function averagePrice() {
    const btnAveragePrice = document.getElementById("btnAveragePrice");
    const box = document.getElementById("averagePriceBox");
    const body = box.querySelector(".card-body");

    btnAveragePrice.addEventListener("click", () => {

        body.innerHTML = "";
        let sum = 0;
        let count = 0;

        for (const book of books) {
            sum += book.price;
            count++;
        }

        const avg = sum / count;

        body.innerHTML = `
            <p class="mb-0">
                평균 도서 가격: <strong>${Math.round(avg).toLocaleString()}원</strong>
            </p>
        `;
    });
}
averagePrice();



function stockAddZeroBook() {
    const btnCheckZeroStock = document.getElementById("btnCheckZeroStock");
    const btnAddStock10 = document.getElementById("btnAddStock10");
    const zeroStockBookBox = document.getElementById("zeroStockBookBox");
    const stockAddMsg = document.getElementById("stockAddMsg");

    let zeroStockBooks = [];

    function renderZeroStockBooks(list) {
        
        zeroStockBookBox.innerHTML = "";
        stockAddMsg.textContent = "";

        if (!list || list.length === 0) {
            zeroStockBookBox.innerHTML = `
                <div class="d-flex gap-3 align-items-center">
                    <img
                        src=""
                        alt="재고가 0인 도서 이미지"
                        class="rounded border"
                        style="width:80px; height:110px; object-fit:cover; display:none;"
                    />
                    <div>
                        <h5 class="mb-1">재고가 0인 도서를 조회해 주세요.</h5>
                        <p class="text-muted mb-0 small">현재 재고가 0인 도서가 없습니다.</p>
                    </div>
                </div>
            `;
            btnAddStock10.disabled = true;
            return;
        }

        // 재고가 0인 도서 출력
        let html = "";

        list.forEach((book) => {
            const imgSrc = book.image
                ? book.image
                : "https://via.placeholder.com/80x110?text=No+Image";

            html += `
                <div class="border rounded p-3 mb-2">
                    <div class="d-flex gap-3 align-items-center">
                        <img
                            src="${imgSrc}"
                            alt="${book.title}"
                            class="rounded border"
                            style="width:80px; height:110px; object-fit:cover;"
                        />
                        <div class="flex-grow-1">
                            <h5 class="mb-1">${book.title}</h5>
                            <div class="small text-muted">
                                author: ${book.author}<br/>
                                category: ${book.category}<br/>
                                price: ${book.price.toLocaleString()}원<br/>
                                stock: ${book.stock}권<br/>
                                image: ${book.image}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        zeroStockBookBox.innerHTML = html;
        btnAddStock10.disabled = false;
        stockAddMsg.textContent = `재고가 0인 도서 ${list.length}권이 조회되었습니다.`;
    }

    btnCheckZeroStock.addEventListener("click", () => {

        zeroStockBooks = books.filter((b) => b.stock === 0);
        renderZeroStockBooks(zeroStockBooks);

    });

    btnAddStock10.addEventListener("click", () => {

        if (!zeroStockBooks || zeroStockBooks.length === 0) return;
        for (const book of zeroStockBooks) {
            book.stock += 10;
        }

        alert("도서가 10권 추가되었습니다.");

        zeroStockBooks = books.filter((b) => b.stock === 0);
        renderZeroStockBooks(zeroStockBooks);
    });
}
stockAddZeroBook();



function addBook() {
    const form = document.getElementById("bookCreateForm");

    const inputTitle = document.getElementById("inputTitle");
    const inputAuthor = document.getElementById("inputAuthor");
    const inputCategory = document.getElementById("inputCategory");
    const inputPrice = document.getElementById("inputPrice");
    const inputStock = document.getElementById("inputStock");
    const inputImage = document.getElementById("inputImage");

    const msg = document.getElementById("bookCreateMsg");

    const DEFAULT_IMAGE = "https://via.placeholder.com/80x110?text=No+Image";

    function isPlaceholderBox(boxId, placeholderText) {
        const box = document.getElementById(boxId);
        const body = box?.querySelector(".card-body");
        if (!body) return true;
        return body.textContent.includes(placeholderText);
    }

    function refreshIfAlreadyShown() {
        if (!isPlaceholderBox("bookListBox", "조회 버튼을 누르면 전체 도서 목록이 표시됩니다.")) {
            document.getElementById("btnLoadBooks")?.click();
        }
        if (!isPlaceholderBox("OnStockbookListBox", "재고가 1권 이상인 도서 목록이 표시됩니다.")) {
            document.getElementById("btnOnStockBooks")?.click();
        }
        if (!isPlaceholderBox("programmingBookListBox", "카테고리가 '프로그래밍'인 도서 목록이 표시됩니다.")) {
            document.getElementById("btnProgrammingBooks")?.click();
        }
        if (!isPlaceholderBox("averagePriceBox", "도서 전체 가격의 평균값이 표시됩니다.")) {
            document.getElementById("btnAveragePrice")?.click();
        }

        const zeroBox = document.getElementById("zeroStockBookBox");
        if (zeroBox && !zeroBox.textContent.includes("재고가 0인 도서를 조회해 주세요.")) {
            document.getElementById("btnCheckZeroStock")?.click();
        }
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        msg.textContent = "";

        const title = inputTitle.value.trim();
        const author = inputAuthor.value.trim();
        const category = inputCategory.value.trim();
        const imageRaw = inputImage.value.trim();
        const price = Number(inputPrice.value);
        const stock = Number(inputStock.value);

        if (!title || !author || !category) {
            msg.textContent = "제목/저자/카테고리를 모두 입력해 주세요.";
            return;
        }
        if (!Number.isFinite(price) || price < 0) {
            msg.textContent = "가격은 0 이상의 숫자로 입력해 주세요.";
            return;
        }
        if (!Number.isFinite(stock) || stock < 0) {
            msg.textContent = "재고는 0 이상의 숫자로 입력해 주세요.";
            return;
        }

        const newBook = {
            title,
            author,
            category,
            price: Math.floor(price),
            stock: Math.floor(stock),
            image: imageRaw ? imageRaw : DEFAULT_IMAGE
        };

        books.push(newBook);

        msg.textContent = `등록 완료: "${newBook.title}" 도서가 추가되었습니다.`;
        form.reset();

        refreshIfAlreadyShown();
    });
}
addBook();
