namespace OnlineStoreBadCode.DTOs;

public class PaymentResponseDto
{
    public bool Success { get; set; }
    public string? TransactionId { get; set; }
    public string? PaypalTransactionId { get; set; }
    public string? ReferenceNumber { get; set; }
    public decimal? Charged { get; set; }
    public string Message { get; set; } = string.Empty;
}