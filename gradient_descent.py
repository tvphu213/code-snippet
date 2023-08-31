import numpy as np
from data_prep import features, targets, features_test, targets_test

def sigmoid(x):
    """
    Tính giá trị sigmoid
    """
    return 1 / (1 + np.exp(-x))

def update_weights(weights, features, targets, learnrate):
    """
    Hoàn thành một vòng lặp gradient descent và trả về trọng số được cập nhật
    """
    del_w = np.zeros(weights.shape)
    # Lặp qua tất cả các hồ sơ, x là đầu vào, y là mục tiêu
    for x, y in zip(features.values, targets):
        # Tính đầu ra của f(h) bằng cách đưa h (tích vô hướng của x và weights) vào hàm kích hoạt (sigmoid).
        output = sigmoid(np.dot(x, weights))

        # Tính lỗi bằng cách trừ đầu ra của mạng từ mục tiêu (y).
        error = y - output

        # Tính error term bằng cách nhân lỗi (error) với gradient. Nhớ rằng gradient của sigmoid f(h) là f(h)*(1−f(h)).
        error_term = error * output * (1 - output)

        # Cập nhật bước trọng số bằng cách nhân error term với đầu vào (x) và cộng vào bước trọng số hiện tại.
        del_w += error_term * x

    n_records = features.shape[0]
    # Cập nhật trọng số bằng cách thêm tỉ lệ học tập nhân với sự thay đổi trọng số chia cho số lượng hồ sơ.
    weights += learnrate * del_w / n_records
    
    return weights

def gradient_descent(features, targets, epochs=1000, learnrate=0.5):
    """
    Thực hiện quy trình gradient descent hoàn chỉnh trên tập dữ liệu cho trước
    """
    # Sử dụng cùng một hạt giống để làm cho việc gỡ lỗi dễ dàng hơn
    np.random.seed(42)
    
    # Khởi tạo lỗi và trọng số
    last_loss = None
    n_features = features.shape[1]
    weights = np.random.normal(scale=1/n_features**.5, size=n_features)

    # Lặp lại việc cập nhật trọng số dựa trên số lượng epochs
    for e in range(epochs):
        weights = update_weights(weights, features, targets, learnrate)

        # In ra lỗi MSE trên tập huấn luyện mỗi 10 epochs.
        # Ban đầu, điều này sẽ in ra cùng một lỗi mỗi lần. Khi tất cả các TODOs được hoàn thành, lỗi MSE sẽ giảm sau mỗi lần in ra.
        if e % (epochs / 10) == 0:
            out = sigmoid(np.dot(features, weights))
            loss = np.mean((out - targets) ** 2)
            if last_loss and last_loss < loss:
                print("Lỗi huấn luyện: ", loss, "  CẢNH BÁO - Lỗi đang tăng")
            else:
                print("Lỗi huấn luyện: ", loss)
            last_loss = loss
            
    return weights

# Tính độ chính xác trên dữ liệu kiểm tra
weights = gradient_descent(features, targets)
tes_out = sigmoid(np.dot(features_test, weights))
predictions = tes_out > 0.5
accuracy = np.mean(predictions == targets_test)
print("Độ chính xác dự đoán: {:.3f}".format(accuracy))
