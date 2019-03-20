function offloader(r, call_try) {
    offload(r, r.variables["offload_args"], 0);
}

function offload(r, poll_id, call_try){
    r.subrequest(
        "/poll/"+poll_id+'/'+call_try,
        {
            method: 'POST',
        },

        function(res) {
            if (res.status >= 200 && res.status < 300) {
                r.return(res.status, res.responseBody);
                return;
            }
            if (call_try > 60) {
                r.return(500);
                return;
            }
            setTimeout(offload, 1000, r, poll_id, call_try + 1)
        }
    );
}
