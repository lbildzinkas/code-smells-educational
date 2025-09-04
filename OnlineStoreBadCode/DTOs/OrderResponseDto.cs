namespace OnlineStoreBadCode.DTOs;

public class OrderResponseDto
{
    public int OrderId { get; set; }
    public string UserId { get; set; } = string.Empty;
    public decimal Total { get; set; }
    public string Status { get; set; } = string.Empty;
    public string PaymentMethod { get; set; } = string.Empty;
    public DateTime OrderDate { get; set; }
}