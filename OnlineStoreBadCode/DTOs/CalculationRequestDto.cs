using System.ComponentModel.DataAnnotations;

namespace OnlineStoreBadCode.DTOs;

public class CalculationRequestDto
{
    [Required(ErrorMessage = "Subtotal is required")]
    [Range(0, double.MaxValue, ErrorMessage = "Subtotal cannot be negative")]
    public decimal Subtotal { get; set; }

    [Required(ErrorMessage = "Type is required")]
    [RegularExpression("^(tax|shipping|discount)$", ErrorMessage = "Type must be tax, shipping, or discount")]
    public string Type { get; set; } = string.Empty;

    public string? Code { get; set; }
}