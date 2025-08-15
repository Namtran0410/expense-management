export class Transform {
    constructor(data) {
        this.data = data || '';
    }

    // Hàm chuyển đổi từ chữ hoặc số sang dạng nghìn
    toThousand() {
        let numberValue;

        if (typeof this.data === 'number') {
            numberValue = this.data; // nếu là số, giữ nguyên
        } else {
            numberValue = Number(String(this.data).replace(/\D/g, "")); // nếu là chuỗi, bỏ chữ
        }

        return numberValue.toLocaleString('vi-VN') + " VNĐ";
    }

    toNumber() {
        let numberValue
        // Nếu là chữ thì chuyển thành số, không thì giữ nguyên
        if (typeof this.data === 'number') {
            numberValue = this.data
        } else {
            numberValue= Number(String(this.data).replace(/\D/g, ""))
        }
        return numberValue 
    }
}
