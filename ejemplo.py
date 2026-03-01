import os
import khipu_tools

khipu_tools.api_key = os.environ.get("KHIPU_API_KEY", "")
khipu_tools.log = "debug"

# banks = khipu_tools.Banks.get()
# print(banks)

# prediction = khipu_tools.Predict.get(
#     payer_email="user@example.com",
#     amount="5000000",
#     currency="CLP",
#     bank_id="Bawdf",
# )
# print(prediction)

# payment = khipu_tools.Payments.create(
#     amount=10000, currency="CLP", subject="Pago de prueba"
# )
# print(payment)

# print(khipu_tools.Payments.get(payment_id="<payment_id>"))
