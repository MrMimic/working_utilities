module WEB

    # Imports
    using HTTP, Sockets

    # Exports
    export get_page


    function download_page_data(url)
        #=
        This function will download data on the url page
        Return depends on response status and catched errors
        =#

        try
            # Get data
            response = HTTP.get(url)
            if typeof(response.status) <: Number && response.status == 200
                return String(response.body)
            end
        # Errors
        catch error
            if typeof(error) == Sockets.DNSError
                println(string("DNS error, please check your URL: ", url))
            end
        end




    end


end
