namespace OnlineStoreBadCode.DTOs;

public class CartResponseDto
{
    public List<object> Items { get; set; } = new List<object>();
    public decimal Total { get; set; }
    public int ItemCount { get; set; }
}