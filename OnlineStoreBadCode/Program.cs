using OnlineStoreBadCode;

// Bad practice: no structured logging, no proper configuration
var builder = WebApplication.CreateBuilder(args);

// Bad practice: no proper service registration
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Bad practice: no CORS configuration
// Bad practice: no authentication/authorization
// Bad practice: no proper error handling middleware
// Bad practice: no request validation
// Bad practice: no rate limiting

var app = builder.Build();

// Bad practice: Swagger in production
app.UseSwagger();
app.UseSwaggerUI();

// Bad practice: no proper exception handling
app.UseHttpsRedirection();

// Bad practice: no request logging
app.MapControllers();

// Bad practice: initializing global state in Program.cs
GlobalVariables.errorMessages.Add("Application started at " + DateTime.Now);

app.Run();
