function user_signup(request_data) {
    $.ajax({
        url: '/user_signup',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        success: function(data) {
            if (data['status'] == 'success') {
                alert("Sign up successful")
                window.location.href = '/signin'; 
            } else {
                alert("Error: " + data.message); 
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.log("AJAX Error:", errorMsg);
            alert("An unexpected error occurred. Please try again.");
        }
    });
}

function user_signin(request_data) {
    $.ajax({
        url: '/user_signin',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        success: function(data) {
            // Check if login was successful
            if(data['status'] == 'Login Successful') {
                window.location.href = '/dashboard';    
                localStorage.setItem('user_id', data['user_id']);
                console.log(localStorage.getItem('user_id'));
            } else {
                window.location.href = '/signup';
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.log("AJAX Error:", errorMsg);
            alert("An unexpected error occurred. Please try again.");
        }
    });
}

function save_user_expense(expense_data) {
    $.ajax({
        url: '/user_expense',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(expense_data),
        success: function(data) {
            if (data['status'] == 'success') {
                alert("Expense added successfully!")
                window.location.href = '/dashboard'; 
            } else {
                alert("Error: " + data.message); 
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.log("AJAX Error:", errorMsg);
            alert("An unexpected error occurred. Please try again.");
        }
    });
}

function save_user_budget(budget_data) {
    $.ajax({
        url: '/user_budget',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(budget_data),
        success: function(data) {
            if (data['status'] == 'success') {
                alert("Budget added successfully!")
                window.location.href = '/dashboard'; 
            } else {
                alert("Error: " + data.message); 
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.log("AJAX Error:", errorMsg);
            alert("An unexpected error occurred. Please try again.");
        }
    });
}

$(document).on("submit", "#signupForm", function(e) {
    e.preventDefault(); 

    let isValid = true;
    $('#signupForm input').each(function() {
        if ($(this).val() === '') {
            isValid = false; 
        }
    });

    if (!isValid) {
        alert("Please fill out all fields.");
        return; 
    }

    var firstName = $("#firstName").val();
    var lastName = $("#lastName").val();
    var email = $("#email").val();
    var password = $("#password").val();

    var request_data = {
        "first_name": firstName,
        "last_name": lastName,
        "email": email,
        "password": password
    };

    user_signup(request_data);
});

    
$(document).on("submit", "#signinForm", function(e) {
        e.preventDefault(); 
    
        var email = $("#email").val();
        var password = $("#password").val();
    
        var request_data = {
            "email": email,
            "password": password
        };
    
        console.log(request_data)
        user_signin(request_data);
    });
    
$(document).ready(function () {
        // Handle click event for the close button
        $('#closeModalBtn').on('click', function () {
            // Redirect to the dashboard
            window.location.href = '/dashboard'; // Replace '/dashboard' with your actual dashboard URL
        });
    });

$(document).on("click", "#saveExpenseBtn", function(e){

    const expense_amount = $("#expenseAmount").val();
    const expense_category = $("#expenseCategory").val();
    const expense_description = $("#expenseDescription").val();
    const expense_date = $("#expenseDate").val();

    const userIdForExpense = localStorage.getItem('user_id');
    console.log("user_id: ",userIdForExpense); 

    var expense_data = {
        "expense_amount": expense_amount,
        "expense_category": expense_category,
        "expense_description": expense_description,
        "expense_date": expense_date,
        "user_id": userIdForExpense
    }

    console.log(expense_data)
    save_user_expense(expense_data);
});

$(document).on("click", "#saveBudgetBtn", function(e){

    var budget_amount = $("#budgetAmount").val();
    var budget_category = $("#budgetCategory").val();

    let userIdForBudget = localStorage.getItem('user_id');
    console.log("user_id: ",userIdForBudget); 

    var budget_data = {
        "user_id": userIdForBudget,
        "budget_amount": budget_amount,
        "budget_category": budget_category
    }

    console.log(budget_data)
    save_user_budget(budget_data);
});

function get_expense_chart_data(selectedYearMonthData) {

    let userIdForExpense = localStorage.getItem('user_id');
    console.log("user_id: ", userIdForExpense);

    request_data = {
        user_id: userIdForExpense,
        selected_year:selectedYearMonthData['selectedYear'],
        selected_month:selectedYearMonthData['selectedMonth']
    }

    $.ajax({
        url: '/get_user_expense_chart',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        success: function(data) {
            console.log("expense data:", data);
            // get_expense_table(data[1]);

            const formattedData = data[1].map(row => ({
                ...row,
                budget_amount: row.budget_amount.toLocaleString('en-IN'), // Format as per Indian locale
                expense_amount: row.expense_amount.toLocaleString('en-IN'),
                saving: row.saving.toLocaleString('en-IN'),
            }));
            
            console.log(formattedData);
            get_expense_table(formattedData);


            
            //Expense Chart by Plotly Js
            const category = data[0].map(item => item.category)
            const expense_amount = data[0].map(item => item.expense_amount)

            const expense_chartData = [{labels:category, values:expense_amount , type:"pie"}];
            Plotly.newPlot("expensePieChart",expense_chartData);

            //budget Chart by Plotly Js
            const budget_amount = data[0].map(item => item.budget_amount)

            const budget_chartData = [{labels:category, values:budget_amount , type:"pie"}];
            Plotly.newPlot("budgetPieChart",budget_chartData);

        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.log("AJAX Error:", errorMsg);
            alert("An unexpected error occurred. Please try again.");
        }
    });
}
// Call the function when the page loads
// document.addEventListener('DOMContentLoaded', (event) => {
//     get_expense_chart_data();
// });

$(document).on("change", "#receipt", function(e) {
    // Get the selected file
    var receiptFile = e.target.files[0];

    if (receiptFile) {
        // Check if the file is an image
        if (receiptFile.type.startsWith("image/")) {
            // Create a FileReader to read the image
            var reader = new FileReader();

            // On file load, set the image source to the preview element
            reader.onload = function(event) {
                $("#imagePreview").attr("src", event.target.result).show();
            };

            // Read the file as a Data URL
            reader.readAsDataURL(receiptFile);
        } else {
            alert("Please select a valid image file.");
            $("#imagePreview").hide();
        }
    } else {
        // Hide preview if no file is selected
        $("#imagePreview").hide();
    }
});


$(document).on("click", "#uploadReceipt", function(e) {
    e.preventDefault(); // Prevent the default form submission

    // Get the selected file
    var receiptFile = $("#receipt")[0].files[0];

    // Check if a file is selected
    if (receiptFile) {
        let userIdForReceipt = localStorage.getItem('user_id'); // Get the user ID from local storage
        console.log("user_id: ", userIdForReceipt); 

        var formData = new FormData();
        formData.append("receipt", receiptFile);
        formData.append("user_id", userIdForReceipt); // Include user ID if needed

        console.log("Uploading receipt data:");
        formData.forEach((value, key) => {
            console.log(`${key}: ${value}`);
        });

        // AJAX request to upload the receipt
        $.ajax({
            url: '/upload_receipt', // Your upload URL
            type: 'POST',
            data: formData,
            processData: false, // Important for file uploads
            contentType: false, // Important for file uploads
            success : function (data) {
                console.log("Received data:", data);
                
                try {
                    var receipt_details = data;
                    console.log("Parsed receipt details:", receipt_details); // Log parsed details
                    
                    if (receipt_details) {
                        populate_receipt_details(receipt_details);
                    } else {
                        console.error("No receipt details found.");
                    }
                } catch (e) {
                    console.error("Failed to parse JSON:", e);
                }
            },
            error: function(xhr, status, error) {
                // Handle the error response
                console.error('Upload failed:', error);
                alert('Failed to upload receipt. Please try again.');
            }
        });
    } else {
        alert('Please select a file to upload.');
    }
});

function populate_receipt_details(receipt_details) {
    var receiptDetailsHtml = '';

    // Create the HTML dynamically for the extracted details
    console.log("Receipt details to populate:", receipt_details);

    // Constructing the HTML with details
    receiptDetailsHtml += `
        <div class="receipt-form">

            <h2>Verify Your Expense Details</h2>

            <label for="receiptAmount"><strong>Amount:</strong></label>
            <input type="text" id="receiptAmount" name="amount" value="${receipt_details['Amount'] || ''}" />

            <label for="receiptCategory"><strong>Category:</strong></label>
            <input type="text" id="receiptCategory" name="category" value="${receipt_details['Category'] || ''}" />

            <label for="receiptDate"><strong>Date:</strong></label>
            <input type="text" id="receiptDate" name="date" value="${receipt_details['Date']}" />

            <label for="receiptDescription"><strong>Description:</strong></label>
            <textarea id="receiptDescription" name="description">${receipt_details['Description'] || ''}</textarea>

            <h4>Edit if necessary, then click 'Save Expenses' to proceed.</h4>
            <p><strong>Note:</strong> Please ensure all fields are filled. If any input box is empty, enter the details manually.</p>

            <button type="submit" class="btn-submit" id="saveReceiptExpenseBtn">Save Expenses</button>
        </div>


    `;

    $("#addExpenseModal").html(receiptDetailsHtml); // Insert the HTML into the page
}

$(document).on("click", "#saveReceiptExpenseBtn", function(e){

    var expense_amount = $("#receiptAmount").val();
    var expense_category = $("#receiptCategory").val();
    var expense_description = $("#receiptDescription").val();
    var expense_date = $("#receiptDate").val();

    var expense_date = $("#receiptDate").val(); // Assume format is DD-MM-YYYY
    var dateParts = expense_date.split("-"); // Split the string by "-"
    var formattedDate = `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`; // Rearrange to YYYY-MM-DD
    console.log(formattedDate); // Output: 2024-12-29


    let userIdForExpense = localStorage.getItem('user_id');
    console.log("user_id: ",userIdForExpense); 

    var expense_data = {
        "expense_amount": expense_amount,
        "expense_category": expense_category,
        "expense_description": expense_description,
        "expense_date": formattedDate,
        "user_id": userIdForExpense
    }

    console.log(expense_data)
    save_user_expense(expense_data);
    
});

function get_expense_and_budget_data(selectedYearMonthData) {

    let userIdForExpense = localStorage.getItem('user_id');
    console.log("user_id: ",userIdForExpense); 

    console.log(selectedYearMonthData)

    request_data = {
        user_id: userIdForExpense,
        selected_year:selectedYearMonthData['selectedYear'],
        selected_month:selectedYearMonthData['selectedMonth']
    }

    console.log(request_data)

    $.ajax({
        url: '/get_expense_and_budget',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        success: function(data) {

            function formatNumber(num) {
                // Convert to float and use toLocaleString for easy formatting
                return parseFloat(num).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            }
            console.log("Expense and Budget data:",data)
            const totalExpenseValue = data[0].total_expense; 
            const totalBudgetValue = data[0].total_budget; 
            const savingValue = totalBudgetValue - totalExpenseValue; 
            
            const totalExpense = formatNumber(totalExpenseValue);
            const totalBudget = formatNumber(totalBudgetValue);
            const saving = formatNumber(savingValue);
            
            $('#totalSpending').text(`${totalExpense}`);
            $('#totalBudget').text(`${totalBudget}`);
            
            let savingText;
            if (savingValue < 0) {
                $('#totalSaving').css('color', 'red');
                savingText = `${formatNumber(savingValue)}`; 
                // $('#savingMessage').text(`You have exceeded your budget. Please review your spending!`);
            } else {
                savingText = `+${formatNumber(savingValue)}`;
                $('#totalSaving').css('color', 'green');
            }
            
            $('#totalSaving').text(savingText);
            
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.log("AJAX Error:", errorMsg);
            alert("An unexpected error occurred. Please try again.");
        }
    });
}

$(document).ready(function() {

    function get_current_year_and_month(){
    //for current year
    const yearSelect = document.getElementById('yearSelect');
    const selectedYear = new Date().getFullYear();
    // console.log(currentYear)
    
    for (let year = selectedYear; year >= 2020; year--) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelect.appendChild(option);

        if (year==selectedYear){
            option.selected = true;
        }
    }

    const selected_year_month_data = {
        selectedYear:selectedYear,
        selectedMonth: null
    }

    get_expense_and_budget_data(selected_year_month_data); 
    get_expense_chart_data(selected_year_month_data);
}

    get_current_year_and_month();

    $(document).on("change", "#yearSelect,#monthSelect", function(e) {
        const selectedYear = $("#yearSelect").val(); // Get the selected value
        console.log("Selected Year:", selectedYear); // Log the selected month
    
        const selectedMonth = $("#monthSelect").val();
        console.log("selected Month:",selectedMonth)
    
        const selected_year_month_data = {
            selectedYear:selectedYear,
            selectedMonth:selectedMonth
        }
    
        // Fetch data for the selected month
        get_expense_and_budget_data(selected_year_month_data); 
        get_expense_chart_data(selected_year_month_data);
    });
});

$(document).on("change","#monthSelect1,#monthSelect2",function(e){

    let userIdForExpense = localStorage.getItem('user_id');
    console.log("user_id: ",userIdForExpense);

    const month1 = $("#monthSelect1").val();
    const month2 = $("#monthSelect2").val();
    const year = $("#yearSelect").val();

    if (month1 && month2) {
        const compare_month = {
            user_id: userIdForExpense,
            year: year,
            month1: month1,
            month2: month2,
        };

        console.log(compare_month);

        // Fetch month comparison data
        get_month_comparison_data(compare_month);
    } else {
        console.log("Both months must be selected to proceed.");
    }

});

function get_month_comparison_data(compare_month){

    $.ajax({
        url:"/get_month_comparison",
        type:"POST",
        datatype:"json",
        contentType:"application/json",
        data: JSON.stringify(compare_month),
        
        success: function (data) {
            console.log(data);
        
            // Extract the months and expenses from the data
            const month1 = data['month1']; // This is the month (e.g., '01' for January)
            const month2 = data['month2']; // This is the month (e.g., '01' for January)
            const month1_expense = data['month1_expense']; // Expense for month1
            const month2_expense = data['month2_expense']; // Expense for month2
        
            // Convert month values to more readable format (e.g., 'January' instead of '01')
            const monthNames = ["January", "February", "March", "April", "May", "June", 
                                "July", "August", "September", "October", "November", "December"];
            const monthArr = [monthNames[parseInt(month1) - 1], monthNames[parseInt(month2) - 1]];
            const monthExpenseArr = [month1_expense, month2_expense];
        
            console.log("Months:", monthArr);
            console.log("Expenses:", monthExpenseArr);
        
            // Check if expenses are valid
            if (month1_expense != null && month2_expense != null) {
                // Create the data for the bar chart
                const monthcomparison_data = [{
                    x: monthArr,
                    y: monthExpenseArr,
                    type: "bar",
                    orientation: "v",
                    marker: { color: "rgba(0,0,255,0.6)" }
                }];
        
                // Layout configuration for the chart
                const layout = {
                    title: "Monthly Expense Comparison",
                    xaxis: { title: "Months" },
                    yaxis: { title: "Expenses"},
                    bargap: 0.6
                };
        
                // Render the chart
                Plotly.newPlot("months_comparison_chart", monthcomparison_data, layout);
            } else {
                console.error("Invalid or missing data for chart rendering");
                alert("Unable to generate chart. Please check the data.");
            }
        },
        error:function(errorMsg){
            console.log("Ajax Error:",errorMsg)
            alert("Unexpexted error.Please try again")
        }
    });


} 

function get_expense_table(data){
  
    var expenseHtml = `
        <table class="expenseTable" border="1">
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Expense Amount</th>
                    <th>Budget Amount</th>
                    <th>Savings</th>
                </tr>
            </thead>
            <tbody>
    `;

    $.each(data, function(index,row){
        expenseHtml += `
            <tr>
                <td>`+row['category']+`</td>
                <td>`+row['expense_amount']+`</td>
                <td>`+row['budget_amount']+`</td>
                <td>`+row['saving']+`</td>
            </tr>
            
        `
    });
        
    expenseHtml += `
            </tbody>
            </table>
    `;

$('#expenseTable').html(expenseHtml);

};

$(document).on("click","#predictedExpenseBtn",function(e){

    let userId = localStorage.getItem('user_id');
    console.log("user_id: ",userId);  

    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    request_data_for_expense_prediction = {
        user_id : userId,
        current_month : currentMonth,
        current_year : currentYear
    }

    get_predicted_expense(request_data_for_expense_prediction)

});


function get_predicted_expense(request_data_for_expense_prediction){

    console.log(request_data_for_expense_prediction)

    $.ajax({
        url:"/get_predicted_expense",
        type:"POST",
        datatype:"json",
        contentType:"application/json",
        data: JSON.stringify(request_data_for_expense_prediction),
        success: function (data) {
            console.log(data);
            $("#predictdExpenseValue").html("<b>Your Next Month Predicted Expense:"+data+"</b>");
        },
        error:function(errorMsg){
            console.log("Ajax Error:",errorMsg)
            alert("Unexpexted error.Please try again")
        }
    })

};
 

















