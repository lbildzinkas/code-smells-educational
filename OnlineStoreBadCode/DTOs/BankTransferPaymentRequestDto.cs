using System.ComponentModel.DataAnnotations;

namespace OnlineStoreBadCode.DTOs;

public class BankTransferPaymentRequestDto : ProcessPaymentRequestDto
{
    [Required(ErrorMessage = "Account number is required")]
    [StringLength(20, MinimumLength = 6, ErrorMessage = "Account number must be between 6 and 20 characters")]
    public string AccountNumber { get; set; } = string.Empty;

    [Required(ErrorMessage = "Routing number is required")]
    [StringLength(9, MinimumLength = 9, ErrorMessage = "Routing number must be 9 digits")]
    public string RoutingNumber { get; set; } = string.Empty;
}