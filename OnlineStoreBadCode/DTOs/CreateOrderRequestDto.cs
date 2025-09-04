using System.ComponentModel.DataAnnotations;

namespace OnlineStoreBadCode.DTOs;

public class CreateOrderRequestDto
{
    [Required(ErrorMessage = "Payment method is required")]
    [RegularExpression("^(credit_card|paypal|bank_transfer)$", ErrorMessage = "Payment method must be credit_card, paypal, or bank_transfer")]
    public string PaymentMethod { get; set; } = string.Empty;
}