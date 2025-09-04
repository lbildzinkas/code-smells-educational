using System.ComponentModel.DataAnnotations;

namespace OnlineStoreBadCode.DTOs;

public class CreditCardPaymentRequestDto : ProcessPaymentRequestDto
{
    [Required(ErrorMessage = "Card number is required")]
    [StringLength(16, MinimumLength = 16, ErrorMessage = "Card number must be 16 digits")]
    public string CardNumber { get; set; } = string.Empty;

    [Required(ErrorMessage = "CVV is required")]
    [StringLength(4, MinimumLength = 3, ErrorMessage = "CVV must be 3 or 4 digits")]
    public string Cvv { get; set; } = string.Empty;

    [Required(ErrorMessage = "Expiry date is required")]
    public string Expiry { get; set; } = string.Empty;
}