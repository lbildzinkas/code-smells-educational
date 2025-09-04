using System.ComponentModel.DataAnnotations;

namespace OnlineStoreBadCode.DTOs;

public abstract class ProcessPaymentRequestDto
{
    [Required(ErrorMessage = "Payment method is required")]
    [RegularExpression("^(credit_card|paypal|bank_transfer)$", ErrorMessage = "Payment method must be credit_card, paypal, or bank_transfer")]
    public string Method { get; set; } = string.Empty;

    [Required(ErrorMessage = "Amount is required")]
    [Range(0.01, double.MaxValue, ErrorMessage = "Amount must be greater than 0")]
    public decimal Amount { get; set; }
}